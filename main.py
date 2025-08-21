from bagpipe.models import Op, Edge
from bagpipe.pipeline import Pipeline


def main():
    p = Pipeline()
    start = 0
    p += (i0 := Op("add x1, x2, x3"))
    p += (i1 := Op("orr x4, x5, x6"))
    p += (i2 := Op("b.eq"))
    i0.D(start + 0), i0.E(start + 1), i0.C(start + 2)
    i1.D(start + 1), i1.E(start + 2), i1.C(start + 3)
    i2.D(start + 2), i2.E(start + 3), i2.C(start + 4)
    p += Edge(i0.D >> i1.D >> i2.D, "red", "in-order-dispatch").set_node_color("pink")
    p += Edge(i0.E >> i1.E, "blue", "data-dependency").set_node_color("lightblue")
    p.draw()


if __name__ == "__main__":
    main()
