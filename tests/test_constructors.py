"""
Unit tests for the Bagpipe DSL.
"""
from bagpipe.models import Op, Node, Pipeline, Edge, Chain


class TestOp:
    """Test the Op class."""

    def test_instruction_creation(self):
        """Test creating an instruction."""
        instruction = Op("test")
        assert instruction.name == "test"
        assert instruction.nodes == {}


class TestNode:
    """Test the Node class."""

    def test_node_creation(self):
        """Test creating a node."""
        node = Node("test", "cycle")
        assert node.label == "test"
        assert node.cycle == "cycle"

    def test_node_creation_in_instruction(self):
        """Test creating a node in an instruction."""
        i0 = Op("test")
        node = i0.d(1)
        assert node.label == "d"
        assert node.cycle == 1
        assert i0.nodes == {"d": node}
        node2 = i0.e(2)
        assert node2.label == "e"
        assert node2.cycle == 2
        assert i0.nodes == {"d": node, "e": node2}


class TestEdge:
    """Test the Edge class."""

    def test_chain_creation(self):
        """Test creating an edge."""
        i0 = Op("test")
        node1 = i0.d(1)
        node2 = i0.e(2)
        i0.f(3)
        edge = node1 >> node2
        edge2 = node2 >> i0.f
        assert edge.nodes == [node1, node2]
        assert edge2.nodes == [node2, i0.f]

    def test_edge_creation(self):
        """Test chaining edges."""
        p = Pipeline()
        p += (i0 := Op("add x1, x2, x3"))
        p += (i1 := Op("orr x4, x5, x6"))
        p += Edge(i0.d(1) >> i1.d(2) >> i1.c(3), "red")
        assert p.edges == [Edge(i0.d >> i1.d >> i1.c, "red")]
        p.draw()

    def test_edge_list_creation(self):
        """Test chaining edges."""
        p = Pipeline()
        i0 = Op("add x1, x2, x3")
        i1 = Op("orr x4, x5, x6")
        p += i0
        p += i1
        i0.add_node(Node("d", 1))
        i1.add_node(Node("d", 2))
        i1.add_node(Node("c", 3))
        p += Edge([i0.d, i1.d, i1.c], "red")
        assert p.edges == [Edge(i0.d >> i1.d >> i1.c, "red")]
        assert p.instructions == [i0, i1]
        p.draw()
