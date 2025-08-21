from bagpipe.models import Op, Edge
from bagpipe.pipeline import Pipeline


def main():
    print("Hello from bagpipe!")
    p = Pipeline()
    p += (i0 := Op("add x1, x2, x3"))
    p += (i1 := Op("orr x4, x5, x6"))
    p += (i2 := Op("b.eq"))
    i0.D(1, "pink"), i0.E(2), i0.C(3)
    i1.D(2), i1.E(3), i1.C(4)
    i2.D(3), i2.E(4), i2.C(5)
    p += Edge(i0.D >> i1.D >> i1.E >> i1.C).set_color("red")
    p += Edge(i1.D >> i2.D >> i2.E >> i2.C).set_color("blue")

    p.draw()


if __name__ == "__main__":
    main()
