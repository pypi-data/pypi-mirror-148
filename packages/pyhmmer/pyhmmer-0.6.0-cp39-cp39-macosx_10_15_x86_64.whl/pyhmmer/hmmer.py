# coding: utf-8
"""Reimplementation of HMMER binaries with the pyHMMER API.
"""

import abc
import contextlib
import collections
import ctypes
import itertools
import io
import queue
import time
import threading
import typing
import os
import multiprocessing

import psutil

from .easel import Alphabet, DigitalSequence, DigitalMSA, MSA, MSAFile, TextSequence, SequenceFile, SSIWriter
from .plan7 import Builder, Background, Pipeline, PipelineSearchTargets, LongTargetsPipeline, TopHits, HMM, HMMFile, Profile, TraceAligner, OptimizedProfile
from .utils import peekable

# the query type for the pipeline
_Q = typing.TypeVar("_Q", HMM, Profile, OptimizedProfile, DigitalSequence, DigitalMSA)
# the model type for the pipeline
_M = typing.TypeVar("_M", HMM, Profile, OptimizedProfile)
# the sequence type for the pipeline
_S = typing.TypeVar("_S", DigitalSequence, DigitalMSA)

# --- Pipeline threads -------------------------------------------------------

class _PipelineThread(typing.Generic[_Q], threading.Thread):
    """A generic worker thread to parallelize a pipelined search.

    Attributes:
        sequence (`pyhmmer.plan7.PipelineSearchTargets`): The target
            sequences to search for hits.
        query_queue (`queue.Queue`): The queue used to pass queries between
            threads. It contains both the query and its index, so that the
            results can be returned in the same order.
        query_count (`multiprocessing.Value`): An atomic counter storing
            the total number of queries that have currently been loaded.
            Passed to the ``callback`` so that an UI can show the total
            for a progress bar.
        hits_queue (`queue.PriorityQueue`): The queue used to pass back
            the `TopHits` to the main thread. The results are inserted
            using the index of the query, so that the main thread can
            pull results in order.
        kill_switch (`threading.Event`): An event flag shared between
            all worker threads, used to notify emergency exit.
        hits_found (`list` of `threading.Event`): A list of event flags,
            such that ``hits_found[i]`` is set when results have been
            obtained for the query of index ``i``. This allows the main
            thread to keep waiting for the right `TopHits` to yield even
            if subsequent queries have already been treated, and to make
            sure the next result returned by ``hits_queue.get`` will also
            be of index ``i``.
        callback (`callable`, optional): An optional callback to be called
            after each query has been processed. It should accept two
            arguments: the query object that was processed, and the total
            number of queries read until now.
        options (`dict`): A dictionary of options to be passed to the
            `pyhmmer.plan7.Pipeline` object wrapped by the worker thread.
        pipeline_class (`type`): The pipeline class to use to search for
            hits. Use `~plan7.LongTargetsPipeline` for `nhmmer`, and
            `~plan7.Pipeline` everywhere else.

    """

    @staticmethod
    def _none_callback(hmm: _Q, total: int) -> None:
        pass

    def __init__(
        self,
        sequences: PipelineSearchTargets,
        query_queue: "queue.Queue[typing.Optional[typing.Tuple[int, _Q]]]",
        query_count: multiprocessing.Value,  # type: ignore
        hits_queue: "queue.PriorityQueue[typing.Tuple[int, TopHits]]",
        kill_switch: threading.Event,
        hits_found: typing.List[threading.Event],
        callback: typing.Optional[typing.Callable[[_Q, int], None]],
        options: typing.Dict[str, typing.Any],
        pipeline_class: typing.Type[Pipeline],
        alphabet: Alphabet,
    ) -> None:
        super().__init__()
        self.options = options
        self.sequences = sequences
        self.pipeline = pipeline_class(alphabet=alphabet, **options)
        self.query_queue: "queue.Queue[typing.Optional[typing.Tuple[int, _Q]]]" = query_queue
        self.query_count = query_count
        self.hits_queue = hits_queue
        self.callback: "typing.Optional[typing.Callable[[_Q, int], None]]" = callback or self._none_callback
        self.kill_switch = kill_switch
        self.hits_found = hits_found
        self.error: typing.Optional[BaseException] = None

    def run(self) -> None:
        while not self.kill_switch.is_set():
            # attempt to get the next argument, with a timeout
            # so that the thread can periodically check if it has
            # been killed, even when the query queue is empty
            try:
                args = self.query_queue.get(timeout=1)
            except queue.Empty:
                continue
            # check if arguments from the queue are a poison-pill (`None`),
            # in which case the thread will stop running
            if args is None:
                self.query_queue.task_done()
                return
            else:
                index, query = args
            # process the arguments, making sure to capture any exception
            # raised while processing the query, and then mark the hits
            # as "found" using a `threading.Event` for each.
            try:
                self.process(index, query)
                self.query_queue.task_done()
            except BaseException as exc:
                self.error = exc
                self.kill()
                return
            finally:
                self.hits_found[index].set()

    def kill(self) -> None:
        self.kill_switch.set()

    def process(self, index: int, query: _Q) -> None:
        hits = self.search(query)
        self.hits_queue.put((index, hits))
        self.callback(query, self.query_count.value)  # type: ignore
        self.pipeline.clear()

    @abc.abstractmethod
    def search(self, query: _Q) -> TopHits:
        return NotImplemented


class _ModelPipelineThread(typing.Generic[_M], _PipelineThread[_M]):
    def search(self, query: _M) -> TopHits:
        return self.pipeline.search_hmm(query, self.sequences)


class _SequencePipelineThread(_PipelineThread[DigitalSequence]):
    def __init__(
        self,
        sequences: PipelineSearchTargets,
        query_queue: "queue.Queue[typing.Optional[typing.Tuple[int, DigitalSequence]]]",
        query_count: multiprocessing.Value,  # type: ignore
        hits_queue: "queue.PriorityQueue[typing.Tuple[int, TopHits]]",
        kill_switch: threading.Event,
        hits_found: typing.List[threading.Event],
        callback: typing.Optional[typing.Callable[[DigitalSequence, int], None]],
        options: typing.Dict[str, typing.Any],
        pipeline_class: typing.Type[Pipeline],
        alphabet: Alphabet,
        builder: Builder,
    ) -> None:
        super().__init__(
            sequences,
            query_queue,
            query_count,
            hits_queue,
            kill_switch,
            hits_found,
            callback,
            options,
            pipeline_class,
            alphabet,
        )
        self.builder = builder

    def search(self, query: DigitalSequence) -> TopHits:
        return self.pipeline.search_seq(query, self.sequences, self.builder)


class _MSAPipelineThread(_PipelineThread[DigitalMSA]):
    def __init__(
        self,
        sequences: PipelineSearchTargets,
        query_queue: "queue.Queue[typing.Optional[typing.Tuple[int, DigitalMSA]]]",
        query_count: multiprocessing.Value,  # type: ignore
        hits_queue: "queue.PriorityQueue[typing.Tuple[int, TopHits]]",
        kill_switch: threading.Event,
        hits_found: typing.List[threading.Event],
        callback: typing.Optional[typing.Callable[[DigitalMSA, int], None]],
        options: typing.Dict[str, typing.Any],
        pipeline_class: typing.Type[Pipeline],
        alphabet: Alphabet,
        builder: Builder,
    ) -> None:
        super().__init__(
            sequences,
            query_queue,
            query_count,
            hits_queue,
            kill_switch,
            hits_found,
            callback,
            options,
            pipeline_class,
            alphabet,
        )
        self.builder = builder

    def search(self, query: DigitalMSA) -> TopHits:
        return self.pipeline.search_msa(query, self.sequences, self.builder)


# --- Search runners ---------------------------------------------------------

class _Search(typing.Generic[_Q], abc.ABC):

    def __init__(
        self,
        queries: typing.Iterable[_Q],
        sequences: typing.Iterable[DigitalSequence],
        cpus: int = 0,
        callback: typing.Optional[typing.Callable[[_Q, int], None]] = None,
        pipeline_class: typing.Type[Pipeline] = Pipeline,
        alphabet: Alphabet = Alphabet.amino(),
        **options # type: typing.Dict[str, object]
    ) -> None:
        self.queries: typing.Iterable[_Q] = queries
        self.cpus = cpus
        self.callback: typing.Optional[typing.Callable[[_Q, int], None]] = callback
        self.options = options
        self.pipeline_class = pipeline_class
        self.alphabet = alphabet
        if isinstance(sequences, PipelineSearchTargets):
            self.sequences = sequences
        else:
            self.sequences = PipelineSearchTargets(sequences)

    @abc.abstractmethod
    def _new_thread(
        self,
        query_queue: "queue.Queue[typing.Optional[typing.Tuple[int, _Q]]]",
        query_count: "multiprocessing.Value[int]",  # type: ignore
        hits_queue: "queue.PriorityQueue[typing.Tuple[int, TopHits]]",
        kill_switch: threading.Event,
        hits_found: typing.List[threading.Event],
    ) -> _PipelineThread[_Q]:
        return NotImplemented

    def _single_threaded(self) -> typing.Iterator[TopHits]:
        # create the queues to pass the HMM objects around, as well as atomic
        # values that we use to synchronize the threads
        hits_found: typing.List[threading.Event] = []
        query_queue = queue.Queue()  # type: ignore
        query_count = multiprocessing.Value(ctypes.c_ulong)
        hits_queue = queue.PriorityQueue()  # type: ignore
        kill_switch = threading.Event()

        # create the thread (to recycle code)
        thread = self._new_thread(query_queue, query_count, hits_queue, kill_switch, hits_found)

        # process each HMM iteratively and yield the result
        # immediately so that the user can iterate over the
        # TopHits one at a time
        for index, query in enumerate(self.queries):
            query_count.value += 1
            thread.process(index, query)
            yield hits_queue.get_nowait()[1]

    def _multi_threaded(self) -> typing.Iterator[TopHits]:
        # create the queues to pass the HMM objects around, as well as atomic
        # values that we use to synchronize the threads
        hits_found: typing.List[threading.Event] = []
        hits_queue = queue.PriorityQueue()  # type: ignore
        query_count = multiprocessing.Value(ctypes.c_ulong)
        kill_switch = threading.Event()
        # the query queue is bounded so that we only feed more queries
        # if the worker threads are waiting for some
        query_queue = queue.Queue(maxsize=self.cpus)  # type: ignore
        # additional type annotations
        query: typing.Optional[_Q]
        index: int

        # create and launch one pipeline thread per CPU
        threads = []
        for _ in range(self.cpus):
            thread = self._new_thread(query_queue, query_count, hits_queue, kill_switch, hits_found)
            thread.start()
            threads.append(thread)

        # catch exceptions to kill threads in the background before exiting
        try:
            # enumerate queries, so that we now the index of each query
            # and we can yield the results in the same order
            queries = enumerate(self.queries)
            # initially feed one query per thread so that they can start
            # working before we enter the main loop
            for (index, query) in itertools.islice(queries, self.cpus):
                query_count.value += 1
                hits_found.append(threading.Event())
                query_queue.put((index, query))
            # alternate between feeding queries to the threads and
            # yielding back results, if available
            hits_yielded = 0
            while hits_yielded < query_count.value:
                # get the next query, or break the loop if there is no query
                # left to process in the input iterator.
                index, query = next(queries, (-1, None))
                if query is None:
                    break
                else:
                    query_count.value += 1
                    hits_found.append(threading.Event())
                    query_queue.put((index, query))
                # yield the top hits for the next query, if available
                if hits_found[hits_yielded].is_set():
                    yield hits_queue.get_nowait()[1]
                    hits_yielded += 1
            # now that we exhausted all queries, poison pill the
            # threads so they stop on their own
            for _ in threads:
                query_queue.put(None)
            # yield remaining results
            while hits_yielded < query_count.value:
                hits_found[hits_yielded].wait()
                yield hits_queue.get_nowait()[1]
                hits_yielded += 1
        except queue.Empty:
            # the only way we can get queue.Empty is if a thread has set
            # the flag for `hits_found[i]` without actually putting it in
            # the queue: this only happens when a background thread raised
            # an exception, so we must chain it
            for thread in threads:
                if thread.error is not None:
                    raise thread.error from None
            # if this is exception is otherwise a bug, make sure to reraise it
            raise
        except BaseException:
            # make sure threads are killed to avoid being stuck,
            # e.g. after a KeyboardInterrupt
            kill_switch.set()
            raise

    def run(self) -> typing.Iterator[TopHits]:
        if self.cpus == 1:
            return self._single_threaded()
        else:
            return self._multi_threaded()


class _ModelSearch(typing.Generic[_M], _Search[_M]):

    def _new_thread(
        self,
        query_queue: "queue.Queue[typing.Optional[typing.Tuple[int, _M]]]",
        query_count: "multiprocessing.Value[int]",  # type: ignore
        hits_queue: "queue.PriorityQueue[typing.Tuple[int, TopHits]]",
        kill_switch: threading.Event,
        hits_found: typing.List[threading.Event],
    ) -> _ModelPipelineThread[_M]:
        return _ModelPipelineThread(
            self.sequences,
            query_queue,
            query_count,
            hits_queue,
            kill_switch,
            hits_found,
            self.callback,
            self.options,
            self.pipeline_class,
            self.alphabet,
        )


class _SequenceSearch(_Search[DigitalSequence]):

    def __init__(
        self,
        builder: Builder,
        queries: typing.Iterable[DigitalSequence],
        sequences: typing.Iterable[DigitalSequence],
        cpus: int = 0,
        callback: typing.Optional[typing.Callable[[DigitalSequence, int], None]] = None,
        pipeline_class: typing.Type[Pipeline] = Pipeline,
        alphabet: Alphabet = Alphabet.amino(),
        **options, # type: typing.Dict[str, object]
    ) -> None:
        super().__init__(queries, sequences, cpus, callback, pipeline_class, alphabet, **options)
        self.builder = builder

    def _new_thread(
        self,
        query_queue: "queue.Queue[typing.Optional[typing.Tuple[int, DigitalSequence]]]",
        query_count: "multiprocessing.Value[int]",  # type: ignore
        hits_queue: "queue.PriorityQueue[typing.Tuple[int, TopHits]]",
        kill_switch: threading.Event,
        hits_found: typing.List[threading.Event],
    ) -> _SequencePipelineThread:
        return _SequencePipelineThread(
            self.sequences,
            query_queue,
            query_count,
            hits_queue,
            kill_switch,
            hits_found,
            self.callback,
            self.options,
            self.pipeline_class,
            self.alphabet,
            self.builder.copy(),
        )


class _MSASearch(_Search[DigitalMSA]):

    def __init__(
        self,
        builder: Builder,
        queries: typing.Iterable[DigitalMSA],
        sequences: typing.Iterable[DigitalSequence],
        cpus: int = 0,
        callback: typing.Optional[typing.Callable[[DigitalMSA, int], None]] = None,
        pipeline_class: typing.Type[Pipeline] = Pipeline,
        alphabet: Alphabet = Alphabet.amino(),
        **options, # type: typing.Dict[str, object]
    ) -> None:
        super().__init__(queries, sequences, cpus, callback, pipeline_class, alphabet, **options)
        self.builder = builder

    def _new_thread(
        self,
        query_queue: "queue.Queue[typing.Optional[typing.Tuple[int, DigitalMSA]]]",
        query_count: "multiprocessing.Value[int]",  # type: ignore
        hits_queue: "queue.PriorityQueue[typing.Tuple[int, TopHits]]",
        kill_switch: threading.Event,
        hits_found: typing.List[threading.Event],
    ) -> _MSAPipelineThread:
        return _MSAPipelineThread(
            self.sequences,
            query_queue,
            query_count,
            hits_queue,
            kill_switch,
            hits_found,
            self.callback,
            self.options,
            self.pipeline_class,
            self.alphabet,
            self.builder.copy(),
        )


# --- hmmsearch --------------------------------------------------------------

def hmmsearch(
    queries: typing.Iterable[_M],
    sequences: typing.Iterable[DigitalSequence],
    cpus: int = 0,
    callback: typing.Optional[typing.Callable[[_M, int], None]] = None,
    **options,  # type: typing.Dict[str, object]
) -> typing.Iterator[TopHits]:
    """Search HMM profiles against a sequence database.

    Arguments:
        queries (iterable of `HMM`, `Profile` or `OptimizedProfile`): The
            query HMMs or profiles to search for in the database.
        sequences (collection of `~pyhmmer.easel.DigitalSequence`): A
            database of sequences to query.
        cpus (`int`): The number of threads to run in parallel. Pass ``1``
            to run everything in the main thread, ``0`` to automatically
            select a suitable number (using `psutil.cpu_count`), or any
            positive number otherwise.
        callback (callable): A callback that is called everytime a query is
            processed with two arguments: the query, and the total number
            of queries. This can be used to display progress in UI.

    Yields:
        `~pyhmmer.plan7.TopHits`: An object reporting *top hits* for each
        query, in the same order the queries were passed in the input.

    Raises:
        `~pyhmmer.errors.AlphabetMismatch`: When any of the query HMMs
        and the sequences do not share the same alphabet.

    Note:
        Any additional arguments passed to the `hmmsearch` function will be
        passed transparently to the `~pyhmmer.plan7.Pipeline` to be created.

    .. versionadded:: 0.1.0

    .. versionchanged:: 0.4.9
       Allow using `Profile` and `OptimizedProfile` queries.

    """
    # count the number of CPUs to use
    _cpus = cpus if cpus > 0 else psutil.cpu_count(logical=False) or multiprocessing.cpu_count()
    runner: _ModelSearch[_M] = _ModelSearch(queries, sequences, _cpus, callback, **options) # type: ignore
    return runner.run()


# --- phmmer -----------------------------------------------------------------

def phmmer(
    queries: typing.Iterable[_S],
    sequences: typing.Iterable[DigitalSequence],
    cpus: int = 0,
    callback: typing.Optional[typing.Callable[[_S, int], None]] = None,
    builder: typing.Optional[Builder] = None,
    **options, # type: typing.Dict[str, object]
) -> typing.Iterator[TopHits]:
    """Search protein sequences against a sequence database.

    Arguments:
        queries (iterable of `DigitalSequence` or `DigitalMSA`): The
            query sequences to search for in the sequence database.
        sequences (collection of `~pyhmmer.easel.DigitalSequence`): A
            database of sequences to query.
        cpus (`int`): The number of threads to run in parallel. Pass ``1`` to
            run everything in the main thread, ``0`` to automatically
            select a suitable number (using `psutil.cpu_count`), or any
            positive number otherwise.
        callback (callable): A callback that is called everytime a query is
            processed with two arguments: the query, and the total number
            of queries. This can be used to display progress in UI.
        builder (`~pyhmmer.plan7.Builder`, optional): A builder to configure
            how the queries are converted to HMMs. Passing `None` will create
            a default instance.

    Yields:
        `~pyhmmer.plan7.TopHits`: A *top hits* instance for each query,
        in the same order the queries were passed in the input.

    Note:
        Any additional keyword arguments passed to the `phmmer` function
        will be passed transparently to the `~pyhmmer.plan7.Pipeline` to
        be created in each worker thread.

    .. versionadded:: 0.2.0

    .. versionchanged:: 0.3.0
       Allow using `DigitalMSA` queries.

    """
    _cpus = cpus if cpus > 0 else psutil.cpu_count(logical=False) or multiprocessing.cpu_count()
    _builder = Builder(Alphabet.amino()) if builder is None else builder

    try:
        _queries: peekable[typing.Union[DigitalSequence, DigitalMSA, HMM]] = peekable(queries)
        _item: typing.Union[DigitalSequence, DigitalMSA, HMM, None] = _queries.peek()
    except StopIteration:
        _item = None

    runner: typing.Union[_SequenceSearch, _MSASearch]
    if _item is None or isinstance(_item, DigitalSequence):
        runner = _SequenceSearch(
            _builder,
            typing.cast(peekable[DigitalSequence], _queries),
            sequences,
            _cpus,
            callback,  # type: ignore
            pipeline_class=Pipeline,
            alphabet=Alphabet.amino(),
            **options
        )
    elif isinstance(_item, DigitalMSA):
        runner = _MSASearch(
            _builder, _queries, sequences, _cpus, callback, pipeline_class=Pipeline, alphabet=Alphabet.amino(), **options   # type: ignore
        )
    else:
        name = type(_item).__name__
        raise TypeError(f"Expected iterable of DigitalSequence or DigitalMSA, found {name}")

    return runner.run()


# --- nhmmer -----------------------------------------------------------------

def nhmmer(
    queries: typing.Iterable[_Q],
    sequences: typing.Iterable[DigitalSequence],
    cpus: int = 0,
    callback: typing.Optional[typing.Callable[[_Q, int], None]] = None,
    builder: typing.Optional[Builder] = None,
    **options, # type: typing.Dict[str, object]
) -> typing.Iterator[TopHits]:
    """Search nucleotide sequences against a sequence database.

    Arguments:
        queries (iterable of `DigitalSequence`, `DigitalMSA`, `HMM`): The
            query sequences or profiles to search for in the sequence
            database.
        sequences (collection of `~pyhmmer.easel.DigitalSequence`): A
            database of sequences to query.
        cpus (`int`): The number of threads to run in parallel. Pass ``1`` to
            run everything in the main thread, ``0`` to automatically
            select a suitable number (using `psutil.cpu_count`), or any
            positive number otherwise.
        callback (callable): A callback that is called everytime a query is
            processed with two arguments: the query, and the total number
            of queries. This can be used to display progress in UI.
        builder (`~pyhmmer.plan7.Builder`, optional): A builder to configure
            how the queries are converted to HMMs. Passing `None` will create
            a default instance.

    Yields:
        `~pyhmmer.plan7.TopHits`: A *top hits* instance for each query,
        in the same order the queries were passed in the input.

    Note:
        Any additional keyword arguments passed to the `nhmmer` function
        will be passed to the `~pyhmmer.plan7.LongTargetsPipeline` created
        in each worker thread. The ``strand`` argument can be used to
        restrict the search on the direct or reverse strand.

    Hint:
        This function is not just `phmmer` for nucleotide sequences; it
        actually uses a `~pyhmmer.plan7.LongTargetsPipeline` internally
        instead of processing each target sequence in its entirety when
        searching for hits. This avoids hitting the maximum target size
        that can be used (100,000 residues), which may be a problem for
        some larger genomes.

    .. versionadded:: 0.3.0

    .. versionchanged:: 0.4.9
       Allow using `Profile` and `OptimizedProfile` queries.

    """
    _cpus = cpus if cpus > 0 else psutil.cpu_count(logical=False) or multiprocessing.cpu_count()
    _builder = Builder(Alphabet.dna()) if builder is None else builder

    try:
        _queries: peekable[_Q] = peekable(queries)
        _item: typing.Optional[_Q] = _queries.peek()
    except StopIteration:
        _item = None

    runner: typing.Union[_SequenceSearch, _MSASearch, _ModelSearch[HMM]]
    if _item is None or isinstance(_item, DigitalSequence):
        runner = _SequenceSearch(
            _builder,
            typing.cast(peekable[DigitalSequence], _queries),
            sequences,
            _cpus,
            callback,  # type: ignore
            pipeline_class=LongTargetsPipeline,
            alphabet=_item.alphabet if _item is not None else Alphabet.dna(),  # type: ignore
            **options,
        )
    elif isinstance(_item, DigitalMSA):
        runner = _MSASearch(
            _builder,
            typing.cast(peekable[DigitalMSA], _queries),
            sequences,
            _cpus,
            callback,
            pipeline_class=LongTargetsPipeline,
            alphabet=_item.alphabet,
            **options,
        )
    elif isinstance(_item, (HMM, Profile, OptimizedProfile)):
        runner = _ModelSearch(
            typing.cast(peekable[HMM], _queries),
            sequences,
            _cpus,
            callback,  # type: ignore
            pipeline_class=LongTargetsPipeline,
            alphabet=_item.alphabet,
            **options,
        )
    else:
        name = type(_item).__name__
        raise TypeError(f"Expected iterable of DigitalSequence, DigitalMSA, HMM, Profile or OptimizedProfile, found {name}")
    return runner.run()


# --- hmmpress ---------------------------------------------------------------

def hmmpress(
    hmms: typing.Iterable[HMM], output: typing.Union[str, "os.PathLike[str]"],
) -> int:
    """Press several HMMs into a database.

    Calling this function will create 4 files at the given location:
    ``{output}.h3p`` (containing the optimized profiles),
    ``{output}.h3m`` (containing the binary HMMs),
    ``{output}.h3f`` (containing the MSV parameters), and
    ``{output}.h3i`` (the SSI index mapping the previous files).

    Arguments:
        hmms (iterable of `~pyhmmer.plan7.HMM`): The HMMs to be pressed
            together in the file.
        output (`str` or `os.PathLike`): The path to an output location
            where to write the different files.

    """
    DEFAULT_L = 400
    path = os.fspath(output)
    nmodel = 0

    with contextlib.ExitStack() as ctx:
        h3p = ctx.enter_context(open("{}.h3p".format(path), "wb"))
        h3m = ctx.enter_context(open("{}.h3m".format(path), "wb"))
        h3f = ctx.enter_context(open("{}.h3f".format(path), "wb"))
        h3i = ctx.enter_context(SSIWriter("{}.h3i".format(path)))
        fh = h3i.add_file(path, format=0)

        for hmm in hmms:
            # create the background model on the first iteration
            if nmodel == 0:
                bg = Background(hmm.alphabet)
                bg.L = DEFAULT_L

            # build the optimized models
            gm = Profile(hmm.M, hmm.alphabet)
            gm.configure(hmm, bg, DEFAULT_L)
            om = gm.optimized()

            # update the disk offsets of the optimized model to be written
            om.offsets.model = h3m.tell()
            om.offsets.profile = h3p.tell()
            om.offsets.filter = h3f.tell()

            # check that hmm has a name
            if hmm.name is None:
                raise ValueError("HMMs must have a name to be pressed.")
            # add the HMM name, and optionally the HMM accession to the index
            h3i.add_key(hmm.name, fh, om.offsets.model, 0, 0)
            if hmm.accession is not None:
                h3i.add_alias(hmm.accession, hmm.name)

            # write the HMM in binary format, and the optimized profile
            hmm.write(h3m, binary=True)
            om.write(h3f, h3p)
            nmodel += 1

    # return the number of written HMMs
    return nmodel


# --- hmmalign ---------------------------------------------------------------

def hmmalign(
    hmm: HMM,
    sequences: typing.Collection[DigitalSequence],
    trim: bool = False,
    digitize: bool = False,
    all_consensus_cols: bool = True,
) -> MSA:
    """Align several sequences to a reference HMM, and return the MSA.

    Arguments:
        hmm (`~pyhmmer.plan7.HMM`): The reference HMM to use for the
            alignment.
        sequences (collection of `~pyhmmer.easel.DigitalSequence`): The
            sequences to align to the HMM.
        trim (`bool`): Trim off any residues that get assigned to
            flanking :math:`N` and :math:`C` states (in profile traces)
            or :math:`I_0` and :math:`I_m` (in core traces).
        digitize (`bool`): If set to `True`, returns a `DigitalMSA`
            instead of a `TextMSA`.
        all_consensus_cols (`bool`): Force a column to be created for
            every consensus column in the model, even if it means having
            all gap character in a column.

    Returns:
        `~pyhmmer.easel.MSA`: A multiple sequence alignment containing
        the aligned sequences, either a `TextMSA` or a `DigitalMSA`
        depending on the value of the ``digitize`` argument.

    See Also:
        The `~pyhmmer.plan7.TraceAligner` class, which lets you inspect the
        intermediate tracebacks obtained for each alignment before building
        a MSA.

    .. versionadded:: 0.4.7

    """
    aligner = TraceAligner()
    traces = aligner.compute_traces(hmm, sequences)
    return aligner.align_traces(
        hmm,
        sequences,
        traces,
        trim=trim,
        digitize=digitize,
        all_consensus_cols=all_consensus_cols
    )


# add a very limited CLI so that this module can be invoked in a shell:
#     $ python -m pyhmmer.hmmsearch <hmmfile> <seqdb>
if __name__ == "__main__":

    import argparse
    import sys

    def _hmmsearch(args: argparse.Namespace) -> int:
        try:
            with SequenceFile(args.seqdb, digital=True) as seqfile:
                sequences: typing.List[DigitalSequence] = list(seqfile)  # type: ignore
        except EOFError as err:
            print(err, file=sys.stderr)
            return 1

        with HMMFile(args.hmmfile) as hmms:
            queries = hmms.optimized_profiles() if hmms.is_pressed() else hmms
            hits_list = hmmsearch(queries, sequences, cpus=args.jobs)  # type: ignore
            for hits in hits_list:
                for hit in hits:
                    if hit.is_reported():
                        print(
                            hit.name.decode(),
                            "-",
                            hit.best_domain.alignment.hmm_accession.decode(),
                            hit.best_domain.alignment.hmm_name.decode(),
                            hit.evalue,
                            hit.score,
                            hit.bias,
                            sep="\t",
                        )

        return 0

    def _phmmer(args: argparse.Namespace) -> int:
        alphabet = Alphabet.amino()

        with SequenceFile(args.seqdb, digital=True, alphabet=alphabet) as seqfile:
            sequences = list(seqfile)

        with SequenceFile(args.seqfile, digital=True, alphabet=alphabet) as queries:
            hits_list = phmmer(queries, sequences, cpus=args.jobs)  # type: ignore

            for hits in hits_list:
                for hit in hits:
                    if hit.is_reported():
                        print(
                            hit.name.decode(),
                            "-",
                            hit.best_domain.alignment.hmm_accession.decode(),
                            hit.best_domain.alignment.hmm_name.decode(),
                            hit.evalue,
                            hit.score,
                            hit.bias,
                            sep="\t",
                        )

        return 0

    def _nhmmer(args: argparse.Namespace) -> int:
        with SequenceFile(args.seqdb, digital=True) as seqfile:
            sequences = list(seqfile)

        with SequenceFile(args.seqfile, digital=True) as queryfile:
            queries = list(queryfile)
            hits_list = nhmmer(queries, sequences, cpus=args.jobs)  # type: ignore
            for hits in hits_list:
                for hit in hits:
                    if hit.is_reported():
                        print(
                            hit.name.decode(),
                            "-",
                            hit.best_domain.alignment.hmm_accession.decode(),
                            hit.best_domain.alignment.hmm_name.decode(),
                            hit.evalue,
                            hit.score,
                            hit.bias,
                            sep="\t",
                        )

        return 0

    def _hmmpress(args: argparse.Namespace) -> int:
        for ext in ["h3m", "h3i", "h3f", "h3p"]:
            path = "{}.{}".format(args.hmmfile, ext)
            if os.path.exists(path):
                if args.force:
                    os.remove(path)
                else:
                    print(f"file {path} already exists")
                    return 1

        with HMMFile(args.hmmfile) as hmms:
            hmmpress(hmms, args.hmmfile)

        return 0

    def _hmmalign(args: argparse.Namespace) -> int:
        try:
            with SequenceFile(args.seqfile, args.informat, digital=True) as seqfile:
                sequences: typing.List[DigitalSequence] = list(seqfile)  # type: ignore
        except EOFError as err:
            print(err, file=sys.stderr)
            return 1

        with HMMFile(args.hmmfile) as hmms:
            hmm = next(hmms)
            if next(hmms, None) is not None:
                print("HMM file contains more than one HMM, exiting", file=sys.stderr)
                return 1

        msa = hmmalign(hmm, sequences, trim=args.trim)
        if args.output == "-":
            with io.BytesIO() as out:
                msa.write(out, args.outformat)
                print(out.getvalue().decode("ascii"), end="")
        else:
            with open(args.output, "wb") as out:
                msa.write(out, args.outformat)

        return 0

    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--jobs", required=False, default=0, type=int)
    subparsers = parser.add_subparsers(
        dest="cmd", help="HMMER command to run", required=True
    )

    parser_hmmsearch = subparsers.add_parser("hmmsearch")
    parser_hmmsearch.set_defaults(call=_hmmsearch)
    parser_hmmsearch.add_argument("hmmfile")
    parser_hmmsearch.add_argument("seqdb")

    parser_phmmer = subparsers.add_parser("phmmer")
    parser_phmmer.set_defaults(call=_phmmer)
    parser_phmmer.add_argument("seqfile")
    parser_phmmer.add_argument("seqdb")

    parser_nhmmer = subparsers.add_parser("nhmmer")
    parser_nhmmer.set_defaults(call=_nhmmer)
    parser_nhmmer.add_argument("seqfile")
    parser_nhmmer.add_argument("seqdb")

    parser_hmmpress = subparsers.add_parser("hmmpress")
    parser_hmmpress.set_defaults(call=_hmmpress)
    parser_hmmpress.add_argument("hmmfile")
    parser_hmmpress.add_argument("-f", "--force", action="store_true")

    parser_hmmalign = subparsers.add_parser("hmmalign")
    parser_hmmalign.set_defaults(call=_hmmalign)
    parser_hmmalign.add_argument(
        "hmmfile",
        metavar="<hmmfile>"
    )
    parser_hmmalign.add_argument(
        "seqfile",
        metavar="<seqfile>",
    )
    parser_hmmalign.add_argument(
        "-o",
        "--output",
        action="store",
        default="-",
        metavar="<f>",
        help="output alignment to file <f>, not stdout"
    )
    parser_hmmalign.add_argument(
        "--trim",
        action="store_true",
        help="trim terminal tails of nonaligned residues from alignment"
    )
    parser_hmmalign.add_argument(
        "--informat",
        action="store",
        metavar="<s>",
        help="assert <seqfile> is in format <s> (no autodetection)",
        choices=SequenceFile._FORMATS.keys(),
    )
    parser_hmmalign.add_argument(
        "--outformat",
        action="store",
        metavar="<s>",
        help="output alignment in format <s>",
        default="stockholm",
        choices=MSAFile._FORMATS.keys(),
    )

    args = parser.parse_args()
    sys.exit(args.call(args))
