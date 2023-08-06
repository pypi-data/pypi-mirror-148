import numpy as np
import opensimplex as simplex


# Note: This script was created to help me understand how to use opensimplex noise2 versus opensimplex noise2array. As it stands, I'm not sure I fully understand, but I believe that noise2array does not really do what I need it to. Leaving this alone for now.

# 2 arrays of x and y values
# [0, 1, 2, 0, 1, 2, 0, 1, 2] # x
# [0, 0, 0, 1, 1, 1, 2, 2, 2] # y

# 1 2D array
#[[(0,0), (1,0), (2, 0)]
# [(0,1), (1,1), (2, 1)]
# [(0,2), (1,2), (2, 2)]]

class NoiseGen1:
    def __init__(self):
        simplex.seed(0)
        self.x = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])
        self.y = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])

    def run(self):
        res = simplex.noise2array(self.x, self.y)

        print("done1")
        return res

class NoiseGen2:
    def __init__(self):
        simplex.seed(0)
        self.two_d_array = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

    def run(self):
        res = []

        for y, row in enumerate(self.two_d_array):
            res.append([])

            for x, coord in enumerate(row):
                res[y].append(simplex.noise2(x, y))

        print("done2")
        return res


if __name__ == "__main__":
    import cProfile

    a = NoiseGen1()
    res1 = a.run()
    #cProfile.run("a.run()", sort="tottime")

    b = NoiseGen2()
    res2 = b.run()
    #cProfile.run("b.run()", sort="tottime")

    print("exiting")