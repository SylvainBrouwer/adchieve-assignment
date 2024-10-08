import distance

def test_distance():
    a = {"lat": 50.066389, "lon": -5.714722}
    b = {"lat": 58.643889, "lon": -3.07}
    return 968 < (distance.haversine_distance(a, b) / 1e3) < 969


def main():
    assert(test_distance())


if __name__ == "__main__":
    main()