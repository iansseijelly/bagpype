import bagpype as bp


def example_simple():

    # Create a pipeline
    p = bp.Pipeline()

    # Add instructions (operations)
    p += (i := bp.Op("add x1, x2, x3"))

    # Add edge and nodes
    p += bp.Edge(i.IF(0) >> i.DE(1) >> i.EX(2) >> i.WB(3), "purple", "simple_pipeline").set_node_color("violet")

    # Visualize the pipeline
    p.draw()


def example_DEC():
    p = bp.Pipeline()
    start = 0
    p += (i0 := bp.Op("add x1, x2, x3"))
    p += (i1 := bp.Op("orr x4, x5, x6"))
    p += (i2 := bp.Op("b.eq"))
    i0.Issue(start + 0), i0.E(start + 1), i0.C(start + 2)
    i1.Issue(start + 1), i1.E(start + 2), i1.C(start + 3)
    i2.Issue(start + 2), i2.E(start + 3), i2.C(start + 4)
    p += bp.Edge(i0.Issue >> i1.Issue >> i2.Issue, "red").set_node_color("pink")
    p += bp.Edge(i0.E >> i1.E, "blue", "data dependency").set_node_color("lightblue")
    p.draw()


def example_program():
    p = bp.Pipeline()

    # Three instructions
    insns = [bp.Op("add x1, x1, x3"),
             bp.Op("sub x4, x1, x5"),  # depends on x1 from i0
             bp.Op("mul x6, x4, x7")]  # depends on x4 from i1

    # Normal pipeline stages
    for i, op in enumerate(insns):
        op.IF(i + 1)
        op.DE(i + 2)
        op.EX(2 * i + 3)
        op.WB(2 * i + 4)
        p += op

    for i in range(len(insns) - 1):
        p += bp.Edge(insns[i].WB >> insns[i + 1].EX, "red", "data hazard").set_node_color("pink")

    p.draw()


if __name__ == "__main__":
    example_simple()
