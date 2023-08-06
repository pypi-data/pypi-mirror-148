from typing import Any, Dict, Optional
from ewokscore.graph import load_graph
from ewokscore.graph.taskgraph import TaskGraph
from ewokscore.node import NodeIdType
from ewokscore.task import Task
from ewokscore.variable import value_from_transfer
from ewokscore import hashing
from ewokscore.graph.analysis import end_nodes
from ewokscore.graph.execute.sequential import instantiate_task_static


def assert_execute_graph_all_tasks(
    taskgraph: TaskGraph,
    expected: Dict[NodeIdType, Any],
    varinfo: Optional[dict] = None,
    execute_graph_result: Optional[Dict[NodeIdType, Task]] = None,
):
    """Check the output of `execute_graph` for each node. When a task is not in `execute_graph_result`,
    it will be instantiated.

    An expected value can be:
        * `None`: task is not executed and therefore does not appear in the results
        * `MISSING_DATA`: task has no output and is therefore cannot be persisted
        * else: task is executed and has output
    """
    taskgraph = load_graph(taskgraph)
    assert not taskgraph.is_cyclic, "Can only check DAG results"

    if execute_graph_result is None:
        execute_graph_result = dict()

    for node in taskgraph.graph.nodes:
        task = execute_graph_result.get(node, None)
        loaded = False
        if task is None:
            assert varinfo, "Need 'varinfo' to load task output"
            task = instantiate_task_static(
                taskgraph.graph, node, tasks=execute_graph_result, varinfo=varinfo
            )
            loaded = True
        assert_task_result(task, node, expected, loaded)


def assert_execute_graph_tasks(
    execute_graph_result: Dict[NodeIdType, Any],
    expected: Dict[NodeIdType, Any],
    varinfo: Optional[dict] = None,
):
    """Check the output of `execute_graph` for each node.

    An expected value can be:
        * `None`: task is not executed and therefore does not appear in the results
        * `MISSING_DATA`: task has no output and is therefore cannot be persisted
        * else: task is executed and has output
    """
    for node_id, expected_result in expected.items():
        if expected_result is None:
            assert node_id not in execute_graph_result
            continue
        result = execute_graph_result[node_id]
        if isinstance(result, Task):
            assert result.done, node_id
            result = result.output_values
        if expected_result == hashing.UniversalHashable.MISSING_DATA:
            assert result == dict(), result
            continue
        for output_name, expected_value in expected_result.items():
            value = result[output_name]
            assert_result(value, expected_value, varinfo=varinfo)


def assert_execute_graph_values(
    execute_graph_result: Dict[str, Any],
    expected: Dict[str, Any],
    varinfo: Optional[dict] = None,
):
    """Check the output of `execute_graph` for the selected outputs of the selected nodes."""
    for output_name, expected_value in expected.items():
        value = execute_graph_result[output_name]
        assert_result(value, expected_value, varinfo=varinfo)


def assert_task_result(task: Task, node_id: NodeIdType, expected: dict, loaded: bool):
    expected_value = expected.get(node_id)
    if expected_value == hashing.UniversalHashable.MISSING_DATA:
        if loaded:
            expected_value = None
        else:
            expected_value = dict()

    if expected_value is None:
        assert not task.done, node_id
    else:
        assert task.done, node_id
        try:
            assert task.output_values == expected_value, node_id
        except AssertionError:
            raise
        except Exception as e:
            raise RuntimeError(f"{node_id} does not have a result") from e


def assert_result(value, expected_value, varinfo: Optional[dict] = None):
    value = value_from_transfer(value, varinfo=varinfo)
    assert value == expected_value


def filter_expected_results(
    ewoksgraph: TaskGraph,
    results: Dict[NodeIdType, Any],
    end_only: bool = False,
    merge: bool = False,
) -> dict:
    if end_only:
        nodes = end_nodes(ewoksgraph.graph)
        results = {k: v for k, v in results.items() if k in nodes}
    else:
        nodes = ewoksgraph.nodes()
    if merge:
        ret = dict()
        for node_id in nodes:
            adict = results.get(node_id)
            if adict:
                ret.update(adict)
        results = ret
    return results
