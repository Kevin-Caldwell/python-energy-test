import uav_energy as ue
import math
from matplotlib import pyplot as plt

if __name__ == "__main__":
    ue.M_CARRY = 30
    ue.V = 10
    ue.sim_init()

    t0 = 0
    t1 = 30000/10
    n = 100000 #int((t1 - t0) / dt) + 1

    dt = (t1 - t0) / (n+1)

    total_energy = 0
    delta_energy = [0]
    t = [t0]

    for i in range(n):
        # ue.V = 3 * math.sin(i/10 )
        t.append(t[-1] + dt)
        ue.update_sim()
        delta_energy.append(ue.power_total() * dt)

    total_energy = sum(delta_energy)
    
    plt.plot(t, delta_energy)
    print(total_energy / 3600000)
    plt.show()
