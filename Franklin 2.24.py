import numpy as np
import control
import matplotlib.pyplot as plt
import os
os.system('clear')  # Para macOS/Linux. Use 'cls' no Windows se quiser.

# 1) Plant matrices
A = np.array([
    [-1, -2, -2],
    [ 0, -1,  1],
    [ 1,  0, -1]
], dtype=float)

B = np.array([[2.0],
              [0.0],
              [1.0]])

C = np.array([[1.0, 0.0, 0.0]])
D = np.zeros((1, 1))

# 2) Choose ζ and ω_n so that %OS < 5% and ts1% < 4.6 s
ζ = 0.8
zeta_omega_n = 1.0         # ζω_n = 1 ⇒ ts1% ≈ 4 s < 4.6 s
ω_n = zeta_omega_n / ζ     # = 1.0 / 0.8 = 1.25

print(f"Using ζ = {ζ:.3f}, so ωₙ = {ω_n:.3f},  ζωₙ = {ζ*ω_n:.3f}")

# 3) Build desired pole‐locations
sigma  = -ζ * ω_n              # = -1.0
omega_d = ω_n * np.sqrt(1 - ζ**2)  # = 0.75


p1 = sigma + 1j * omega_d      # ≃ -1 + j0.75
p2 = sigma - 1j * omega_d      # ≃ -1 - j0.75
p3 = -4.0                       # third pole far to the left

p1 = -0.77 + 1j * 1.47      # ≃ -1 + j0.75
p2 = -0.77 - 1j * 1.47      # ≃ -1 - j0.75
p3 = -1.45                      # third pole far to the left

desired_poles = [p1, p2, p3]
print("Desired poles:", np.round(desired_poles, 4))

# 4) Compute state‐feedback K
K = control.place(A, B, desired_poles)
print("Computed K =", np.round(K, 4))

# 5) Build A_cl and compute Nbar for unity‐DC‐gain
A_cl = A - B.dot(K)
Acl_inv = np.linalg.inv(A_cl)
denom = C.dot(Acl_inv).dot(B)    # this is a 1×1 matrix
Nbar = -1.0 / float(denom)       # scalar

print("Computed Nbar =", np.round(float(Nbar), 4))

# 6) Form the closed‐loop SS with pre‐gain
A_cl = A - B.dot(K)
B_cl = B #* float(Nbar)
C_cl = C.copy()
D_cl = np.zeros((1,1))

sys_cl = control.ss(A_cl, B_cl, C_cl, D_cl)

G_cl = control.ss2tf(sys_cl)

print(sys_cl)
print(G_cl)

# 7) Simulate unit‐step
t = np.linspace(0, 10, 1000)
t_out, y_out = control.step_response(sys_cl, T=t)

# 8) Plot result
plt.figure(figsize=(7,4))
plt.plot(t_out, y_out, lw=2, label='y(t)')
plt.axhline(1.0, color='k', ls='--', label='Reference = 1')
plt.ylim([-1, 1.2])
plt.xlabel("Time (sec)")
plt.ylabel("y(t)")
plt.title("Closed‐Loop Step Response (with Nbar pre‐gain)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# 9) Compute overshoot and 1% settling time
y_max = np.max(y_out)
percent_overshoot = (y_max - 1.0) * 100

upper = 1.0 * 1.01
lower = 1.0 * 0.99
settling_time = None
for idx in range(len(y_out)-1, -1, -1):
    if (y_out[idx] > upper) or (y_out[idx] < lower):
        if idx + 1 < len(t_out):
            settling_time = t_out[idx + 1]
        else:
            settling_time = t_out[-1]
        break

print(f"\n→ Percent overshoot  ≈ {percent_overshoot:.2f}%")
print(f"→ Approximate 1% settling time ≈ {settling_time:.2f} s")
