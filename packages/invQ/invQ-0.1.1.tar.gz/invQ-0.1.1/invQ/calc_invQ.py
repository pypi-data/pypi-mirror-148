import numpy as np
import json, rowan, math

def invQuat(input_file, equivQ_file):
    with open(input_file) as g:
        data = json.load(g)

    with open(equivQ_file) as f:
        equiv_data = json.load(f)

    refQ = data["refQ"]
    orientations = data["Orientations"]
    equivQ = equiv_data["Equivalent_orientations"]
    sorted_orientations = []
    theta_array = []
    for i in range(len(orientations)):   # choosing particles one by one
        eqivQ = []
        for t in range(len(equivQ)):   # operation of each invariant quaternion on each particle
            eqivQ.append(rowan.normalize(rowan.multiply(orientations[i], equivQ[t])))   # Operating equivalent orientations on particle i

        angles = []
        for q1 in range(len(eqivQ)):   # Calculating angles among these quats
            quat_multiplication = rowan.multiply(rowan.conjugate(refQ), eqivQ[q1])
            quat_multiplication = rowan.normalize(quat_multiplication)
            angles.append(np.rad2deg(2*math.acos(quat_multiplication[0])))

        theta = np.min(angles)  # min angle
        theta_array.append(theta)
        for a in range(len(angles)):
            if angles[a] == theta:  # effective quaternion corresponding to the minimum angle
                sorted_orientations.append(eqivQ[a].tolist())
                break

    output_data = {}
    output_data["refQ"] = refQ
    output_data["equivQ"] = sorted_orientations
    output_data["Angles"] = theta_array
    with open('output.json', 'w') as outfile:
        json.dump(output_data, outfile, indent=4)