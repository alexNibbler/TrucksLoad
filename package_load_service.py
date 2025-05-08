from itertools import combinations
from collections import namedtuple
from functools import cache
import math

from models import Package, Truck
from exceptions import NotEnoughPackages, TooBigPackages


@cache
def volume(length, width, height):
    return length * width * height

def load_packages_by_volume(packages: list[Package], trucks: list[Truck]):
    package_volumes = [(p, volume(p.length, p.width, p.height)) for p in packages]
    total_pkg_volume = sum(v for _, v in package_volumes)

    package_too_small = True
    BestTruck = namedtuple("BestTruck", "truck volume_diff") # (truck_object, truck_volume - total_package_volume)
    best_truck: BestTruck = BestTruck(truck = None, volume_diff=math.inf)
    for truck in trucks:
        truck_volume = volume(truck.length, truck.width, truck.height)
        if total_pkg_volume < 0.8 * truck_volume:
            continue

        if total_pkg_volume > truck_volume:
            package_too_small = False
            continue

        cur_volume_diff = truck_volume - total_pkg_volume
        if best_truck.volume_diff > cur_volume_diff:
            best_truck = (truck, cur_volume_diff)

    if best_truck.truck:
        for pkg in packages:
            pkg.truck_id = best_truck.truck.id
        best_truck.truck.available = False
    elif package_too_small:
        raise NotEnoughPackages()

    # If packages were not placed and are load is not too small
    # that means there are trucks with smaller volume than total_pkg_volume and we should arrange partial load

    higher_volume_trucks = [] # list of tuples (truck, truck_volume)
    for t in trucks:
        v = volume(t.length, t.width, t.height)
        if v < total_pkg_volume:
            higher_volume_trucks.append((t,v))

    # sort desc according to volume (2nd element of the tuple)
    higher_volume_trucks.sort(key=lambda x: x[1], reverse=True)

    BestLoad = namedtuple("BestLoad", "truck used_volume packages")
    best_load = BestLoad(truck=None, used_volume=0, packages=None)

    for truck_volume_pair in higher_volume_trucks:
        truck_vol = truck_volume_pair[1]
        if truck_vol < best_load.used_volume:
            break       # as trucks list is sorted we will not find a better solution to carry more packages

        for r in range(1, len(package_volumes) + 1):
            for subset in combinations(package_volumes, r):
                pkgs, vols = zip(*subset)
                used_volume = sum(vols)
                if truck_vol >= used_volume >= 0.8 * truck_vol:
                    if used_volume > best_load.used_volume:
                        best_load = BestLoad(truck_volume_pair[0], used_volume, pkgs)

    if best_load.truck:
        for pkg in best_load.packages:
            pkg.truck_id = best_truck.truck.id
        best_truck.truck.available = False

    # endpoint should return the truck and the list of assigned and not assigned packages
    left_packages = [p for p in packages if p not in best_load.packages]

    # if still no load could be formed, that means each package is too big for available trucks
    raise TooBigPackages()
