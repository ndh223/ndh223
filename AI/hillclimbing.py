import json
import random
from enum import Enum
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

class ParkingConfig:
    SIZE_COMPATIBILITY = {
        "small": ["small", "medium", "large"],
        "medium": ["medium", "large"],
        "large": ["large"]
    }
    
    MISMATCH_TYPE_PENALTY = 10
    SIZE_MISMATCH_PENALTY = 5
    HEIGHT_MISMATCH_PENALTY = 100
    SHORT_TERM_THRESHOLD = 2
    UNASSIGNED_VEHICLE_PENALTY = 50


    VEHICLE_SIZE_PRIORITY = {
        "large": 0,
        "medium": 1, 
        "small": 2
    }


class SpotType(Enum):
    UNDERGROUND = "underground"
    ROOFTOP = "rooftop"


class ParkingSpots:
    def __init__(self, id: int, spot_type: SpotType, size: str, driver_difficulty: float):
        self.id = id
        self.spot_type = spot_type.value
        self.size = size
        self.driver_difficulty = driver_difficulty
        self.occupied = None


class Vehicle:
    def __init__(self, id: str, size: str, parking_time: float):
        self.id = id
        self.size = size
        self.parking_time = parking_time


def _add_vehicle(vehicles_list, form):
    vid = (form.get("vehicle_id") or "").strip()
    vsize = (form.get("vehicle_size") or "small").lower()
    try:
        vtime = float(form.get("parking_time", 1.0))
        if vtime < 0:
            return "Thời gian đỗ không được âm.", vehicles_list
    except:
        vtime = 1.0

    if not vid:
        return "Vui lòng nhập biển số xe.", vehicles_list
    if vsize not in ("small", "medium", "large"):
        return "Kích thước xe không hợp lệ.", vehicles_list
    if any(v.id == vid for v in vehicles_list):
        return f"Xe {vid} đã tồn tại.", vehicles_list

    vehicles_list.append(Vehicle(vid, vsize, vtime))
    return f"Đã thêm xe {vid}.", vehicles_list


def _remove_vehicle(vehicles_list, form):
    rid = (form.get("remove_vehicle_id") or "").strip()
    new_list = [v for v in vehicles_list if v.id != rid]
    if len(new_list) != len(vehicles_list):
        return f"Đã xóa xe {rid}.", new_list
    return f"Không tìm thấy xe {rid}.", vehicles_list


def _clear_vehicles(vehicles_list, _form):
    return "Đã xóa tất cả xe.", []


ACTION_HANDLERS = {
    "add": _add_vehicle,
    "remove": _remove_vehicle,
    "clear": _clear_vehicles,
}


def is_compatibility(vehicle, spot):
    vsize = vehicle.size.lower()
    if vsize == "large" and spot.spot_type == SpotType.UNDERGROUND.value:
        return False
    return spot.size in ParkingConfig.SIZE_COMPATIBILITY.get(vsize, [])


def calculate_cost(vehicles, spots):
    cost = 0
    vehicle_dict = {v.id: v for v in vehicles}
    occupied_spots = sum(1 for s in spots if s.occupied is not None)
    empty_costs = len(spots) - occupied_spots
    cost += empty_costs

    assigned_vehicles = set(s.occupied for s in spots if s.occupied is not None)
    unassigned_vehicles = len(vehicles) - len(assigned_vehicles)
    cost += unassigned_vehicles * ParkingConfig.UNASSIGNED_VEHICLE_PENALTY

    for spot in spots:
        if spot.occupied:
            veh = vehicle_dict.get(spot.occupied)
            if not veh:
                continue
            if spot.size != veh.size:
                cost += ParkingConfig.SIZE_MISMATCH_PENALTY

            is_short_term = veh.parking_time <= ParkingConfig.SHORT_TERM_THRESHOLD
            if (is_short_term and spot.spot_type == SpotType.UNDERGROUND.value) or \
               (not is_short_term and spot.spot_type == SpotType.ROOFTOP.value):
                cost += ParkingConfig.MISMATCH_TYPE_PENALTY

            if is_short_term and spot.driver_difficulty > 1:
                cost += spot.driver_difficulty - 1

            if veh.size == "large" and spot.spot_type == SpotType.UNDERGROUND.value:
                cost += ParkingConfig.HEIGHT_MISMATCH_PENALTY

    return max(cost, 0)


def initialize_vehicle(vehicles, spots):
    for spot in spots:
        spot.occupied = None

    def size_key(v):
        return ParkingConfig.VEHICLE_SIZE_PRIORITY.get(v.size.lower(), 3)

    vehicles_sorted = sorted(vehicles, key=size_key)
    available_spots = list(spots)

    for vehicle in vehicles_sorted:
        compatible_spots = [s for s in available_spots if is_compatibility(vehicle, s) and s.occupied is None]
        if compatible_spots:
            best_spot = min(compatible_spots, key=lambda s: s.driver_difficulty)
            best_spot.occupied = vehicle.id

def hill_climbing(vehicles, spots, max_iterations=100):
    current_spots = [ParkingSpots(s.id, SpotType(s.spot_type), s.size, s.driver_difficulty) for s in spots]
    initialize_vehicle(vehicles, current_spots)
    current_cost = calculate_cost(vehicles, current_spots)

    for _ in range(max_iterations):
        improved = False
        for s1 in current_spots:
            for s2 in current_spots:
                if s1 == s2 or not s1.occupied or not s2.occupied:
                    continue
                new_spots = [ParkingSpots(s.id, SpotType(s.spot_type), s.size, s.driver_difficulty) for s in current_spots]
                for old, new in zip(current_spots, new_spots):
                    new.occupied = old.occupied
                s1_idx = next(i for i, s in enumerate(new_spots) if s.id == s1.id)
                s2_idx = next(i for i, s in enumerate(new_spots) if s.id == s2.id)
                new_spots[s1_idx].occupied, new_spots[s2_idx].occupied = s2.occupied, s1.occupied
                new_cost = calculate_cost(vehicles, new_spots)
                if new_cost < current_cost:
                    current_cost = new_cost
                    current_spots = new_spots
                    improved = True
                    break
            if improved:
                break
        if not improved:
            break
    return current_spots, current_cost

spots = [
    ParkingSpots(1, SpotType.UNDERGROUND, "medium", 1),
    ParkingSpots(2, SpotType.ROOFTOP, "large", 2.0),
    ParkingSpots(3, SpotType.UNDERGROUND, "medium", 3.0),
    ParkingSpots(4, SpotType.UNDERGROUND, "small", 4.0),
    ParkingSpots(5, SpotType.ROOFTOP, "small", 4.5),
]
vehicles = []

#-------------Setting web---------------
@app.route('/', methods=['GET', 'POST'])
def index():
    global vehicles

    message = None

    if request.method == "POST":
        action = (request.form.get("action") or "").strip()
        handler = ACTION_HANDLERS.get(action)
        if handler:
            message, vehicles = handler(vehicles, request.form)

    if not vehicles:
        optimized_spots, cost, initial_cost = [], 0, 0
        assigned_vehicles = set()
    else:

        initial_spots = [ParkingSpots(s.id, SpotType(s.spot_type), s.size, s.driver_difficulty) for s in spots]
        initialize_vehicle(vehicles, initial_spots)
        initial_cost = calculate_cost(vehicles, initial_spots)

        optimized_spots, optimized_cost = hill_climbing(vehicles, spots)
        cost = optimized_cost  # giữ nguyên tên cũ để tương thích template

        assigned_vehicles = set(s.occupied for s in optimized_spots if s.occupied)
        unassigned = [v.id for v in vehicles if v.id not in assigned_vehicles]
        if unassigned:
            message = f"Không còn chỗ cho xe: {', '.join(unassigned)}"

    return render_template(
        'index.html',
        spots=optimized_spots,
        cost=cost,                
        initial_cost=initial_cost, 
        assigned=len(assigned_vehicles),
        total=len(vehicles),
        vehicles=vehicles,
        message=message
    )



if __name__ == "__main__":
    app.run(debug=False)
