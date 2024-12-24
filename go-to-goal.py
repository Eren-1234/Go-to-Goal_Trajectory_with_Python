import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Sabitler
R = 0.1       # Tekerlek çapı (m)
L = 0.35      # Taban genişliği (m)
K_p = 0.5     # Doğrusal hız için kazanç
K_theta = 2.0 # Açısal hız için kazanç
dt = 0.1      # Zaman adımı

# Başlangıç ve hedef pozisyonlar
x, y, theta = 0, 0, 0           
x_goal, y_goal = 15, 20         

# Simülasyon verilerini saklamak için listeler
x_data, y_data = [x], [y]

# Zaman sayacı için bir değişken
time_elapsed = 0

# Animasyon ayarları
fig, ax = plt.subplots()
ax.set_xlim(-5, 20)
ax.set_ylim(-5, 25)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.plot(x_goal, y_goal, "ro", label="Hedef Konum")
robot_path, = ax.plot([], [], "b-", label="Robotun Yolu")
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes, color="purple")
ax.legend()
ax.grid()

# Robotun yönünü gösterecek ok
robot_arrow = ax.arrow(x, y, 0.5 * np.cos(theta), 0.5 * np.sin(theta),
                       head_width=0.2, head_length=0.3, fc='red', ec='red')

# Hareket güncelleme fonksiyonu
def update(frame):
    global x, y, theta, time_elapsed, robot_arrow

    # Hedef açıyı ve yönelim hatası
    theta_goal = np.arctan2(y_goal - y, x_goal - x)
    error_theta = theta_goal - theta

    # Hedefe olan mesafe
    distance_to_goal = np.sqrt((x_goal - x) ** 2 + (y_goal - y) ** 2)

    
    if distance_to_goal < 0.1:
        ani.event_source.stop()
        return robot_path, time_text, robot_arrow

    # Doğrusal ve açısal hızları
    v = K_p * distance_to_goal
    omega = K_theta * error_theta

    # Sağ ve sol tekerlek açısal hızları
    omega_r = (2 * v + omega * L) / (2 * R)
    omega_l = (2 * v - omega * L) / (2 * R)

    # Yeni pozisyonları güncelle
    x += (R / 2) * (omega_r + omega_l) * np.cos(theta) * dt
    y += (R / 2) * (omega_r + omega_l) * np.sin(theta) * dt
    theta += (R / L) * (omega_r - omega_l) * dt

    # Zamanı güncelle
    time_elapsed += dt

    # Verileri güncelle
    x_data.append(x)
    y_data.append(y)
    robot_path.set_data(x_data, y_data)
    time_text.set_text(f"Time Elapsed: {time_elapsed:.1f} s")

    # Robotun yön oku güncelle
    robot_arrow.remove()  
    robot_arrow = ax.arrow(x, y, 0.5 * np.cos(theta), 0.5 * np.sin(theta),
                           head_width=0.2, head_length=0.3, fc='red', ec='red')

    return robot_path, time_text, robot_arrow

# Animasyon fonksiyonu
ani = FuncAnimation(fig, update, frames=500, interval=100, blit=True)

plt.title("Go-to-Goal Robot Hareketi (Animasyon)")
plt.show()
