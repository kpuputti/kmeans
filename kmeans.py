from matplotlib import pyplot as plt
import math
import random
import sys


def plot(file_name, *variables):
    """Save given iterables of (x, y) coordinate tuples into a file."""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for var in variables:
        xvals = [v[0] for v in var]
        yvals = [v[1] for v in var]
        ax.plot(xvals, yvals, 'o')
    fig.savefig(file_name)


def random_cluster(midpoint, n):
    """Return a list of n (x, y) coordinate tuples around the given
    midpoint with Gaussian noise added to the coordinates."""
    return [(midpoint[0] + random.gauss(0, 2.5),
             midpoint[1] + random.gauss(0, 2.5))
            for _ in xrange(n)]


def distance(point1, point2):
    """Return the Euclidian distance between the given points."""
    return math.sqrt(pow(point2[0] - point1[0], 2) +
                     pow(point2[1] - point1[1], 2))


def closest(datum, midpoints):
    """Return the index of the closest point in the midpoints."""
    closest_index = None
    closest_distance = None
    for i, point in enumerate(midpoints):
        dist = distance(datum, point)
        if closest_index is None or dist < closest_distance:
            closest_index = i
            closest_distance = dist
    return closest_index


def avg(li):
    """Return the average of the given list."""
    return sum(li) / float(len(li))


def get_midpoint(data):
    """Calculate the average midpoint from the data."""
    return (avg([d[0] for d in data]),
            avg([d[1] for d in data]))


def kmeans(data, k, iterations=100):
    """Calculate k clusters from the given data using the kmeans
    algorithm in the given iterations."""
    clusters = [set() for _ in xrange(k)]
    midpoints = random.sample(data, k)

    # init data to clusters
    for datum in data:
        i = random.choice(range(k))
        clusters[i].add(datum)

    for _ in xrange(iterations):
        for datum in data:

            # remove from clusters
            for c in clusters:
                try:
                    c.remove(datum)
                except KeyError:
                    pass

            # get closest midpoint index
            closest_index = closest(datum, midpoints)

            # add to the new cluster
            clusters[closest_index].add(datum)

        # update midpoints
        midpoints = [get_midpoint(c) for c in clusters]

    return clusters


def cluster_randomly(data, k):
    """Cluster the given data into k clusters randomly."""
    clusters = []
    for _ in xrange(k - 1):
        sample = set(random.sample(data, len(data) / k))
        data -= sample
        clusters.append(sample)
    clusters.append(data)
    assert len(clusters) == k
    return clusters


def test():
    data = set(random_cluster((5, 10), 100) +
               random_cluster((10, 30), 100) +
               random_cluster((20, 20), 100) +
               random_cluster((30, 30), 100))
    plot('output/data.png', data)
    clusters = cluster_randomly(data, 4)
    plot('output/clustered_random.png', *clusters)

    for i in range(100):
        clusters = kmeans(data, 4, i)
        plot('output/clustered_kmeans_%d.png' % i, *clusters)

    clusters = kmeans(data, 4, 1000)
    plot('output/clustered_kmeans_1000.png', *clusters)


def main():
    test()
    return 0


if __name__ == '__main__':
    sys.exit(main())
