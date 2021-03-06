# Eduardo Caicedo - Luis Woelke
# Práctica 3
import numpy as np
from matplotlib import pylab as plb

# valores iniciales
n = 361
r1 = 2.22
theta1 = 206
thetapab = 31
r2 = 1
r3 = 2.06
r4 = 2.33
rap = 3.06
rbp = np.sqrt((rap ** 2) + (r3 ** 2) - (2 * rap * r3) * plb.cos(np.radians(thetapab)))
r1_c = r1 * plb.cos(np.radians(theta1))
r1_s = r1 * plb.sin(np.radians(theta1))
mc = 50
theta2_dot = (25 * plb.pi) / 60
x = np.zeros((361, 1))
# Arreglos para la posicion
y1 = np.zeros((361, 1))
y2 = np.zeros((361, 1))
# Arreglos para la velocidad
y1_dot = np.zeros((361, 1))
y2_dot = np.zeros((361, 1))
# Arreglos para la aceleracion
y1_dot2 = np.zeros((361, 1))
y2_dot2 = np.zeros((361, 1))
# Arreglos para posición del punto P
y1_dot3 = np.zeros((361, 1))
y2_dot3 = np.zeros((361, 1))
y = np.zeros((361, 1))
# Arreglo para el torque en eslabon 2
TsM = np.zeros((121, 1))
# Arreglo para Fuerzas en O2
Fo2x_M = np.zeros((121, 1))
Fo2y_M = np.zeros((121, 1))
# Recorrido de theta 2 para 360 grados
for i in range(n):
    theta2_o = 0 + i
    deltatheta3 = 1
    deltatheta4 = 1
    theta3_o = 340
    theta4_o = 280
    rp_o = 1
    rp_c_o = 1
    rp_s_o = 1
    thetabp_o = 1
    # Iteracion por cada angulo de theta 2 con un error admisible de 0.001 (metodo de Newton)
    while deltatheta3 > 0.001 or deltatheta4 > 0.001:
        f1i = r1_c + (r2 * plb.cos(np.radians(theta2_o))) + (r3 * plb.cos(np.radians(theta3_o))) - (
                r4 * plb.cos(np.radians(theta4_o)))
        f2i = r1_s + (r2 * plb.sin(np.radians(theta2_o))) + (r3 * plb.sin(np.radians(theta3_o))) - (
                r4 * plb.sin(np.radians(theta4_o)))
        J11 = -r3 * plb.sin(np.radians(theta3_o))
        J12 = r4 * plb.sin(np.radians(theta4_o))
        J21 = r3 * plb.cos(np.radians(theta3_o))
        J22 = -r4 * plb.cos(np.radians(theta4_o))
        Jinv21 = ((-J21 / J11) / (J22 - (J21 * J12 / J11)))
        Jinv22 = (1 / (J22 - (J21 * J12 / J11)))
        Jinv11 = (1 / J11) - ((J12 / J11) * Jinv21)
        Jinv12 = -((J12 / J11) * Jinv22)
        theta3_corr = theta3_o - ((Jinv11 * f1i) + (Jinv12 * f2i))  # Valores n+1 para angulos de theta 3 y 4
        theta4_corr = theta4_o - ((Jinv21 * f1i) + (Jinv22 * f2i))
        beta1 = 360 - theta3_corr
        beta2 = rap * plb.sin(np.radians(thetapab)) / rbp  # Variación de angulo de vector rap
        beta2deg = 180 - np.degrees(plb.arcsin(beta2))
        thetabp = 180 - beta2deg - beta1
        thetabp_o = thetabp
        deltatheta3 = abs(theta3_o - theta3_corr)  # Error admisible
        deltatheta4 = abs(theta4_o - theta4_corr)
        theta3_o = theta3_corr
        theta4_o = theta4_corr
        # Segundo lazo vectorial para obtener la posicion del Punto P
        rp_c = (rbp * plb.cos(np.radians(thetabp))) + (r2 * plb.cos(np.radians(theta2_o))) + (
                    r3 * plb.cos(np.radians(theta3_o)))
        rp_s = (rbp * plb.sin(np.radians(thetabp))) + (r2 * plb.sin(np.radians(theta2_o))) + (
                    r3 * plb.sin(np.radians(theta3_o)))
        rp = np.sqrt((rp_c ** 2) + (rp_s ** 2))
        rp_o = rp
        rp_c_o = rp_c
        rp_s_o = rp_s

    # Recuperación de datos de posición P y sus componentes con respecto al eje x y eje y
    y[i, 0] = rp_o
    y1_dot3[i, 0] = rp_c_o
    y2_dot3[i, 0] = rp_s_o

    # Recuperación de datos de theta 3 y 4 a partir de la variación de theta 2 de 0 a 360 con 1 unidad de paso
    y1[i, 0] = theta3_o
    y2[i, 0] = theta4_o
    x[i, 0] = i
    # Cálculo y recuperación de datos de velocidad angular de eslabones 3 y 4
    theta3_dot = (theta2_dot * r2 * (plb.cos(np.radians(theta2_o)) + (
            (r2 * plb.sin(np.radians(theta2_o))) / (plb.sin(np.radians(theta4_o)))))) / (r3 * (
            -plb.cos(np.radians(theta3_o)) + (plb.sin(np.radians(theta3_o)) / plb.tan(np.radians(theta4_o)))))
    theta4_dot = ((r2 * theta2_dot * plb.sin(np.radians(theta2_o))) + (
            r3 * theta3_dot * plb.sin(np.radians(theta3_o)))) / (r4 * plb.sin(np.radians(theta4_o)))
    y1_dot[i, 0] = theta3_dot
    y2_dot[i, 0] = theta4_dot
    # Cálculo y recuperación de datos de aceleración angular de eslabones 3 y 4
    theta3_dot2 = ((r2 * (theta2_dot ** 2) * plb.cos(np.radians(theta2_o))) + (
                r3 * (theta3_dot ** 2) * plb.cos(np.radians(theta3_o)))
                   + (((r2 * (theta2_dot ** 2) * plb.sin(np.radians(theta2_o)))
                       + (r3 * (theta3_dot ** 2) * plb.sin(np.radians(theta3_o)))
                       - (r4 * (theta4_dot ** 2) * plb.sin(np.radians(theta4_o)))) * (plb.tan(np.radians(theta4_o))))
                   - (r4 * theta4_dot * plb.cos(np.radians(theta4_o)))) / ((-r3 * plb.sin(np.radians(theta3_o)))
                                                                           + (r3 * plb.cos(
                np.radians(theta3_o)) * plb.tan(np.radians(theta4_o))))
    theta4_dot2 = ((r2 * (theta2_dot ** 2) * plb.sin(np.radians(theta2_o))) - (
                r3 * theta3_dot2 * plb.cos(np.radians(theta3_o)))
                   + (r3 * (theta3_dot ** 2) * plb.sin(np.radians(theta3_o)))
                   - (r4 * (theta4_dot ** 2) * plb.sin(np.radians(theta4_o)))) \
                  / -(r4 * plb.cos(np.radians(theta4_o)))
    y1_dot2[i, 0] = theta3_dot2
    y2_dot2[i, 0] = theta4_dot2
    # Calculando la velocidad del punto P
    thetap = np.degrees(plb.arctan(rp_s_o / rp_c_o))
    rp_dot = ((rbp * theta3_dot * (
                plb.cos(np.radians(thetabp_o)) - (plb.sin(np.radians(thetabp_o)) / plb.tan(np.radians(thetap)))))
              + (r3 * theta3_dot * (
                        plb.cos(np.radians(theta3_o)) - (plb.sin(np.radians(theta3_o)) / plb.tan(np.radians(thetap)))))
              + (r2 * theta2_dot * (
                        plb.cos(np.radians(theta2_o)) - (plb.sin(np.radians(theta2_o)) / plb.tan(np.radians(thetap)))))) \
             / (plb.sin(np.radians(thetap)) + (plb.cos(np.radians(thetap)) / plb.tan(np.radians(thetap))))
    thetap_dot = ((rp_dot * plb.cos(np.radians(thetap))) + (rbp * theta3_dot * plb.sin(np.radians(thetabp_o)))
                  + (r3 * theta3_dot * plb.sin(np.radians(theta3_o)))
                  + (r2 * theta2_dot * plb.sin(np.radians(theta2_o)))) / (rp_o * plb.sin(np.radians(thetap)))
    # rp_dotM[i, 0] = rp_dot
    # Calculando la aceleracion del punto P
    rp_dot2 = ((rbp * theta3_dot2 * (plb.cos(np.radians(thetabp_o)) -
                                     ((rp_dot / (rp_o * plb.tan(np.radians(thetap)))) * plb.sin(
                                         np.radians(thetabp_o))))) +
               (r3 * theta3_dot2 * (plb.cos(np.radians(theta3_o)) -
                                    ((rp_dot / (rp_o * plb.tan(np.radians(thetap)))) * plb.sin(
                                        np.radians(theta3_o))))) -
               (rbp * (theta3_dot ** 2) * (plb.sin(np.radians(thetabp_o)) - (
                           (rp_dot / (rp_o * plb.tan(np.radians(thetap)))) * plb.cos(np.radians(thetabp_o)))))
               - (r3 * (theta3_dot ** 2) * (plb.sin(np.radians(theta3_o)) - (
                        (rp_dot / (rp_o * plb.tan(np.radians(thetap)))) * plb.cos(np.radians(theta3_o)))))
               - (r2 * (theta2_dot ** 2) * (plb.sin(np.radians(theta2_o)) - (
                        (rp_dot / (rp_o * plb.tan(np.radians(thetap)))) * plb.cos(np.radians(theta2_o)))))
               + (rp_o * (thetap_dot ** 2) * (plb.sin(np.radians(thetap)) + (
                        (rp_dot / (rp_o * plb.tan(np.radians(thetap)))) * plb.cos(np.radians(thetap)))))
               - (2 * (rp_dot * thetap_dot * plb.cos(np.radians(thetap))))
               + ((rp_dot / (rp_o * plb.tan(np.radians(thetap)))) * (
                        2 * (rp_dot * thetap_dot * plb.sin(np.radians(thetap)))))) / \
              (plb.sin(np.radians(thetap)) + (
                          (rp_dot / (rp_o * plb.tan(np.radians(thetap)))) * plb.cos(np.radians(thetap))))
    # rp_dot2M[i, 0] = rp_dot2
    if i > 199 and i < 321:
        i = i - 200
        # Torque aplicado en eslabon 2 por trabajo virtual
        Ts = -(3 * (50 / 386.4) * rp_dot * rp_dot2) / theta2_dot
        TsM[i, 0] = Ts
        # Reacciones de eslabon 2 con la bancada
        Fo2x = (-(3 * (50 / 386.4) * rp_dot2 * rbp * plb.sin(np.radians(theta4_o)))
                / (2 * rap * (plb.sin(np.radians(theta2_o)) - plb.cos(np.radians(theta2_o))))) * plb.cos(
            np.radians(theta2_o))
        Fo2y = -(-(3 * (50 / 386.4) * rp_dot2 * rbp * plb.sin(np.radians(theta4_o)))
                 / (2 * rap * (plb.sin(np.radians(theta2_o)) - plb.cos(np.radians(theta2_o))))) * plb.sin(
            np.radians(theta2_o))
        Fo2x_M[i, 0] = Fo2x
        Fo2y_M[i, 0] = Fo2y
x_F = x[200:321]

# Gráficos
# Posición P con respecto a theta 2
plb.plot(y1_dot3, y2_dot3, label='Posicion P')
plb.legend(loc='lower left')
plb.xlabel('Posicion x [in]')
plb.ylabel('Posicion y [in]')
plb.grid()
plb.title('Posicion P')
plb.show()
# Posicion componentes x y y del punto P con respecto a theta 2
plb.plot(x, y1_dot3, label='Posicion x de P')
plb.plot(x, y2_dot3, label='Posicion y de P')
plb.legend(loc='center left')
plb.xlabel('theta 2 [grad]')
plb.ylabel('Posicion [in]')
plb.title('Posicion')
plb.grid()
plb.show()
# Posición angular de eslabones 3 y 4 con respecto a theta 2
plb.plot(x, y1, label='Theta 3')
plb.plot(x, y2, label='Theta 4')
plb.legend(loc='upper left')
plb.xlabel('theta 2 [grad]')
plb.ylabel('theta [grad]')
plb.title('Posicion')
plb.grid()
plb.show()
# Velocidad angular de eslabones 3 y 4 con respecto a theta 2
plb.plot(x, y1_dot, label='Velocidad angular de eslabón 3')
plb.plot(x, y2_dot, label='Velocidad angular del eslabón 4')
plb.legend(loc='upper right')
plb.xlabel('Theta 2 [rad/s]')
plb.ylabel('w [rad/s]')
plb.title('Velocidad angular')
plb.grid()
plb.show()
# Aceleración angular de eslabones 3 y 4 con respecto a theta 2
plb.plot(x, y1_dot2, label='Aceleración angular de eslabón 3')
plb.plot(x, y2_dot2, label='Aceleración angular del eslabón 4')
plb.legend(loc='upper right')
plb.xlabel('Theta 2 [rad/s]')
plb.ylabel('Alpha [rad/s]')
plb.title('Aceleración angular')
plb.grid()
plb.show()
# Torque ejercicio en eslabon 2 con respecto a theta 2
plb.plot(x_F, TsM)
plb.xlabel('Theta 2 [rad/s]')
plb.ylabel('Torque [lb-in]')
plb.title('Torque ejercido en eslabón 2')
plb.grid()
plb.show()
# Reacciones en eslabon 2 con respecto a theta 2
plb.plot(x_F, Fo2x_M, label='Reacción en x')
plb.plot(x_F, Fo2y_M, label='Reacción en y')
plb.legend(loc='upper right')
plb.xlabel('Theta 2 [rad/s]')
plb.ylabel('Fo2 [lb]')
plb.title('Reacciones en la bancada del eslabón 2')
plb.grid()
plb.show()

