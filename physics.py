import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import numpy as np
import io
import math
def calculate_resonance_position_and_width(spectrum_file):
    with open(spectrum_file, 'r') as f:
        data = [line.split() for line in f.readlines()]
    wavelengths = np.array([float(line[0]) for line in data])  
    intensities = np.array([float(line[1]) for line in data])
    max_intensity_index = np.argmax(intensities)
    max_intensity_wavelength = wavelengths[max_intensity_index]
    half_max_intensity = intensities[max_intensity_index] / 2
    left_half_max_index = np.argmin(np.abs(intensities[:max_intensity_index] - half_max_intensity))
    right_half_max_index = np.argmin(np.abs(intensities[max_intensity_index:] - half_max_intensity)) + max_intensity_index
    width = wavelengths[right_half_max_index] - wavelengths[left_half_max_index]
    
    
    plt.figure()
    plt.plot(wavelengths, intensities)
    plt.axvline(max_intensity_wavelength, color='r', linestyle='dashed', linewidth=2)
    plt.axvline(wavelengths[left_half_max_index], color='g', linestyle='dashed', linewidth=2)
    plt.axvline(wavelengths[right_half_max_index], color='g', linestyle='dashed', linewidth=2)
    plt.xlabel('Длина волны (нм)')
    plt.ylabel('Интенсивность')
    plt.title('Спектр резонанса')
    
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()  
    
    return max_intensity_wavelength, width, buf

def calculate_fluence(average_power, beam_radius, repetition_rate):
    fluence = average_power / (np.pi * (beam_radius ** 2) * repetition_rate)
    return fluence

def convert_energy_to_wavelength(energy_eV):
    
    h = 4.135667696e-15  
    c = 299792458  
    wavelength_nm = (h * c) / (energy_eV * 1e-9)
    return wavelength_nm

def convert_wavelength_to_energy(wavelength_nm):
    
    h = 4.135667696e-15  
    c = 299792458  
    energy_eV = (h * c) / (wavelength_nm * 1e-9)
    return energy_eV

def convert_frequency_to_wavelength(frequency_THz):
    
    c = 299792458  
    wavelength_nm = (c / (frequency_THz * 1e12)) * 1e9
    return wavelength_nm

def convert_wavelength_to_frequency(wavelength_nm):
    
    c = 299792458  
    frequency_THz = (c / (wavelength_nm * 1e-9)) * 1e-12
    return frequency_THz
def calculate_force(mass, acceleration):
    return mass * acceleration

def calculate_momentum(mass, velocity):
    return mass * velocity

def calculate_energy_mass_equivalence(mass):
    c = 299792458  
    return mass * (c ** 2)

def calculate_work(force, distance):
    return force * distance

def calculate_power(work, time):
    return work / time

def calculate_kinetic_energy(mass, velocity):
    return 0.5 * mass * (velocity ** 2)

def calculate_potential_energy(mass, height, g=9.81):
    return mass * g * height


def calculate_heat(mass, specific_heat, delta_temperature):
    return mass * specific_heat * delta_temperature

def ideal_gas_law(pressure, volume, n, temperature):
    R = 8.314  
    return pressure * volume == n * R * temperature

def first_law_thermodynamics(delta_u, q, w):
    return delta_u == q - w


def electric_force(charge, electric_field):
    return charge * electric_field

def ohms_law(voltage, current):
    return voltage / current

def electric_power(voltage, current):
    return voltage * current

def lorentz_force(charge, velocity, magnetic_field):
    return charge * velocity * magnetic_field


def refractive_index(c, v):
    return c / v

def thin_lens_equation(f, u, v):
    return 1/f == 1/u + 1/v

def diffraction_maximum(d, theta, m, wavelength):
    return d * math.sin(theta) == m * wavelength


def photon_energy(h, f):
    return h * f

def de_broglie_wavelength(h, p):
    return h / p

def heisenberg_uncertainty(delta_x, delta_p):
    h_bar = 1.0545718e-34  
    return delta_x * delta_p >= h_bar / 2


def radioactive_decay(N0, lambda_val, t):
    return N0 * math.exp(-lambda_val * t)


def wave_velocity(frequency, wavelength):
    return frequency * wavelength

def wave_equation(A, omega, k, x, t):
    return A * math.sin(omega * t - k * x)


def hydrostatic_pressure(rho, g, h):
    return rho * g * h

def archimedes_force(rho, V, g=9.81):
    return rho * V * g


def time_dilation(t, v, c=299792458):
    return t / math.sqrt(1 - (v**2 / c**2))

def length_contraction(l, v, c=299792458):
    return l * math.sqrt(1 - (v**2 / c**2))


def gravitational_force( m1, m2, r):
    G  =  6.67384
    return G * (m1 * m2) / (r ** 2)


