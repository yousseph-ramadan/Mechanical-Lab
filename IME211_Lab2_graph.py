import matplotlib.pyplot as plt
import numpy as np


num_materials = int(input("Enter the number of materials you want to compare: "))
T0 = float(input("Enter initial baseline temperature T0 (°C): "))
num_points = int(input(f"Enter the number of measured points for each material: "))

materials_data = []

for m in range(num_materials):
  print(f"\n================ Material {m+1} ================")
  name = input("Enter material name (e.g., Polyethylene, Steel): ")
  
  
  dT = [0.0]
  dL = [0.0]

  for i in range(num_points):
    T_val = float(input(f"  Point {i+1} - Temperature T (°C): "))
    dL_val = float(input(f"  Point {i+1} - Thermal Expansion ΔL (mm): "))

    dT.append(T_val - T0)
    dL.append(dL_val)

  materials_data.append({
      "name": name,
      "dT": np.array(dT),
      "dL": np.array(dL),
  })


plt.figure(figsize=(10, 6))

for mat in materials_data:
  dT = mat["dT"]
  dL = mat["dL"]

  
  A = np.column_stack((dT, np.ones(len(dT))))
  b = dL.reshape(-1, 1)

  
  At = A.T
  AtA = np.dot(At, A)
  Atb = np.dot(At, b)

  
  solution = np.linalg.solve(AtA, Atb)
  slope = solution[0][0]
  intercept = solution[1][0]

  
  x_line = np.linspace(0, max(dT), 100)
  y_line = slope * x_line + intercept

  
  (point_plot,) = plt.plot(dT, dL, "o", label=f"{mat['name']} points")
  color = point_plot.get_color()  # Re-use the same color for the fit line
  plt.plot(
      x_line,
      y_line,
      "-",
      color=color,
      label=f"{mat['name']} (m = {slope:.4f} mm/°C)",
  )

plt.xlabel("Temperature Change ΔT (°C)")
plt.ylabel("Thermal Expansion ΔL (mm)")
plt.title("Thermal Expansion Comparison")
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()
plt.savefig("thermal_expansion_comparison.png", dpi=300)