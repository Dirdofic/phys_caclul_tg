import asyncio
import pandas as pd
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import os
import pytz
from physics import *

API_TOKEN = 'YOUR_BOT_TOKEN'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    waiting_for_energy_wavelength_choice = State()
    waiting_for_energy = State()
    waiting_for_wavelength = State()
    waiting_for_frequency_wavelength_choice = State()
    waiting_for_frequency = State()
    waiting_for_fluence_power = State()
    waiting_for_fluence_radius = State()
    waiting_for_fluence_rate = State()
    waiting_for_spectrum_file = State()
    waiting_for_feedback = State()
    waiting_for_physics_category = State()
    waiting_for_physics_calculation = State()
    waiting_for_force = State()
    waiting_for_momentum = State()
    waiting_for_energy_mass = State()
    waiting_for_work = State()
    waiting_for_power = State()
    waiting_for_kinetic_energy = State()
    waiting_for_potential_energy = State()
    waiting_for_heat = State()
    waiting_for_ideal_gas = State()
    waiting_for_electric_force = State()
    waiting_for_ohms_law = State()
    waiting_for_electric_power = State()
    waiting_for_lorentz_force = State()
    waiting_for_refractive_index = State()
    waiting_for_thin_lens = State()
    waiting_for_photon_energy = State()
    waiting_for_de_broglie = State()
    waiting_for_radioactive_decay = State()
    waiting_for_wave_velocity = State()
    waiting_for_hydrostatic_pressure = State()
    waiting_for_archimedes_force = State()
    waiting_for_time_dilation = State()
    waiting_for_length_contraction = State()
    waiting_for_gravitational_force = State()



main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(KeyboardButton("Энергия ⟷ Длина волны"))
main_keyboard.add(KeyboardButton("Частота ⟷ Длина волны"))
main_keyboard.add(KeyboardButton("Рассчитать флюенцию"))
main_keyboard.add(KeyboardButton("Рассчитать резонанс"))
main_keyboard.add(KeyboardButton("Другие"))
def save_feedback(username, function, comment):
    moscow_tz = pytz.timezone('Europe/Moscow')
    
    moscow_time = datetime.datetime.now(moscow_tz)
    feedback_data = {
        'username': [username],
        'function': [function],
        'comment': [comment],
        'timestamp': [moscow_time]
    }
    df = pd.DataFrame(feedback_data)
    
    if os.path.exists('feedback.csv'):
        df.to_csv('feedback.csv', mode='a', header=False, index=False)
    else:
        df.to_csv('feedback.csv', index=False)

async def ask_for_feedback(message: types.Message, state: FSMContext, function_name: str):
    await state.update_data(last_function=function_name)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Да"), KeyboardButton("Нет"))
    await Form.waiting_for_feedback.set()
    await message.reply("Хотите оставить отзыв или комментарий?", reply_markup=keyboard)

@dp.message_handler(state=Form.waiting_for_feedback)
async def process_feedback(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await message.reply("Пожалуйста, напишите ваш отзыв или комментарий:")
        await Form.waiting_for_feedback.set()
    elif message.text.lower() == "нет":
        await state.finish()
        await message.reply("Спасибо! Выберите операцию:", reply_markup=main_keyboard)
    else:
        data = await state.get_data()
        last_function = data.get('last_function', 'Unknown')
        save_feedback(message.from_user.username or str(message.from_user.id), last_function, message.text)
        await state.finish()
        await message.reply("Спасибо за ваш отзыв! Выберите операцию:", reply_markup=main_keyboard)
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для физических расчетов. Выберите операцию:", reply_markup=main_keyboard)

@dp.message_handler(text="Энергия ⟷ Длина волны")
async def energy_wavelength_choice(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Энергия → Длина волны"))
    keyboard.add(KeyboardButton("Длина волны → Энергия"))
    keyboard.add(KeyboardButton("Назад"))
    await Form.waiting_for_energy_wavelength_choice.set()
    await message.reply("Выберите тип перевода:", reply_markup=keyboard)

@dp.message_handler(state=Form.waiting_for_energy_wavelength_choice)
async def process_energy_wavelength_choice(message: types.Message, state: FSMContext):
    if message.text == "Энергия → Длина волны":
        await Form.waiting_for_energy.set()
        await message.reply("Введите энергию фотона в кэВ:")
    elif message.text == "Длина волны → Энергия":
        await Form.waiting_for_wavelength.set()
        await message.reply("Введите длину волны в нм:")
    elif message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
    else:
        await message.reply("Пожалуйста, используйте кнопки для выбора.")

@dp.message_handler(state=Form.waiting_for_energy)
async def process_energy(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        energy_keV = float(message.text)
        energy_eV = energy_keV * 1000
        wavelength = convert_energy_to_wavelength(energy_eV)
        frequency = convert_wavelength_to_frequency(wavelength)
        wavenumber = 1 / (wavelength * 1e-7)          
        response = f"Энергия: {energy_keV:.3f} кэВ ({energy_eV:.3f} эВ)\n"
        response += f"Длина волны: {wavelength:.3f} нм\n"
        response += f"Частота: {frequency:.3f} ТГц\n"
        response += f"Волновое число: {wavenumber:.2f} см^-1"
        
        await message.reply(response)
        await ask_for_feedback(message, state, "energy_to_wavelength")
    except ValueError:
        await message.reply("Пожалуйста, введите корректное число.")

@dp.message_handler(state=Form.waiting_for_wavelength)
async def process_wavelength(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        wavelength = float(message.text)
        frequency = convert_wavelength_to_frequency(wavelength)
        energy = convert_wavelength_to_energy(wavelength)
        wavenumber = 1 / (wavelength * 1e-7)          
        response = f"Длина волны: {wavelength:.3f} нм\n"
        response += f"Частота: {frequency:.3f} ТГц\n"
        response += f"Энергия: {energy:.3f} эВ\n"
        response += f"Волновое число: {wavenumber:.2f} см^-1"
        
        await message.reply(response)
        await ask_for_feedback(message, state, "wavelength_to_frequency_and_energy")
    except ValueError:
        await message.reply("Пожалуйста, введите корректное число.")



@dp.message_handler(text="Частота ⟷ Длина волны")
async def frequency_wavelength_choice(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Частота → Длина волны"))
    keyboard.add(KeyboardButton("Длина волны → Частота"))
    keyboard.add(KeyboardButton("Назад"))
    await Form.waiting_for_frequency_wavelength_choice.set()
    await message.reply("Выберите тип перевода:", reply_markup=keyboard)

@dp.message_handler(state=Form.waiting_for_frequency_wavelength_choice)
async def process_frequency_wavelength_choice(message: types.Message, state: FSMContext):
    if message.text == "Частота → Длина волны":
        await Form.waiting_for_frequency.set()
        await message.reply("Введите частоту излучения в ТГц:")
    elif message.text == "Длина волны → Частота":
        await Form.waiting_for_wavelength.set()
        await message.reply("Введите длину волны в нм:")
    elif message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
    else:
        await message.reply("Пожалуйста, используйте кнопки для выбора.")


@dp.message_handler(state=Form.waiting_for_frequency)
async def process_frequency(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        frequency = float(message.text)
        wavelength = convert_frequency_to_wavelength(frequency)
        energy = convert_wavelength_to_energy(wavelength)
        wavenumber = 1 / (wavelength * 1e-7)          
        response = f"Частота: {frequency:.3f} ТГц\n"
        response += f"Длина волны: {wavelength:.3f} нм\n"
        response += f"Энергия: {energy:.3f} эВ\n"
        response += f"Волновое число: {wavenumber:.2f} см^-1"
        
        await message.reply(response)
        await ask_for_feedback(message, state, "frequency_to_wavelength")
    except ValueError:
        await message.reply("Пожалуйста, введите корректное число.")






@dp.message_handler(text="Рассчитать флюенцию")
async def fluence_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Отмена"))
    await Form.waiting_for_fluence_power.set()
    await message.reply("Введите среднюю мощность лазера в Вт или нажмите 'Отмена' для возврата в главное меню:", reply_markup=keyboard)

@dp.message_handler(state=Form.waiting_for_fluence_power)
async def process_fluence_power(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.reply("Операция отменена. Выберите другую операцию:", reply_markup=main_keyboard)
        return

    try:
        power = float(message.text)
        await state.update_data(power=power)
        await Form.waiting_for_fluence_radius.set()
        await message.reply("Введите радиус лазерного пучка в мм или нажмите 'Отмена':")
    except ValueError:
        await message.reply("Пожалуйста, введите корректное число или нажмите 'Отмена'.")

@dp.message_handler(state=Form.waiting_for_fluence_radius)
async def process_fluence_radius(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.reply("Операция отменена. Выберите другую операцию:", reply_markup=main_keyboard)
        return

    try:
        radius = float(message.text)
        await state.update_data(radius=radius)
        await Form.waiting_for_fluence_rate.set()
        await message.reply("Введите частоту повторения лазерного излучения в Гц или нажмите 'Отмена':")
    except ValueError:
        await message.reply("Пожалуйста, введите корректное число или нажмите 'Отмена'.")

@dp.message_handler(state=Form.waiting_for_fluence_rate)
async def process_fluence_rate(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.reply("Операция отменена. Выберите другую операцию:", reply_markup=main_keyboard)
        return

    try:
        rate = float(message.text)
        data = await state.get_data()
        power = data['power']
        radius = data['radius'] / 10  
        fluence = calculate_fluence(power, radius, rate)
        
        response = f"Флюенция: {fluence:.3f} Дж/см²\n"
        response += f"Мощность: {power:.3f} Вт\n"
        response += f"Радиус пучка: {radius*10:.3f} мм\n"
        response += f"Частота повторения: {rate:.3f} Гц\n"
        response += f"Энергия импульса: {power/rate:.3f} Дж"
        
        await message.reply(response)
        await ask_for_feedback(message, state, "fluence")
    except ValueError:
        await message.reply("Пожалуйста, введите корректное число или нажмите 'Отмена'.")
@dp.message_handler(text="Рассчитать резонанс")
async def resonance_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Отмена"))
    await Form.waiting_for_spectrum_file.set()
    await message.reply("Пожалуйста, отправьте файл спектра в формате .txt или нажмите 'Отмена' для возврата в главное меню.", reply_markup=keyboard)

@dp.message_handler(state=Form.waiting_for_spectrum_file, content_types=['document', 'text'])
async def process_spectrum_file(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.reply("Операция отменена. Выберите другую операцию:", reply_markup=main_keyboard)
        return

    if message.document and message.document.mime_type == 'text/plain':
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        
        os.makedirs(f'user_files/{message.from_user.id}', exist_ok=True)
        
        await bot.download_file(file_path, f'user_files/{message.from_user.id}/spectrum.txt')
        
        try:
            max_intensity_wavelength, width, buf = calculate_resonance_position_and_width(f'user_files/{message.from_user.id}/spectrum.txt')
            
            energy = convert_wavelength_to_energy(max_intensity_wavelength)
            frequency = convert_wavelength_to_frequency(max_intensity_wavelength)
            wavenumber = 1 / (max_intensity_wavelength * 1e-7)              
            response = f"Положение резонанса: {max_intensity_wavelength:.3f} нм\n"
            response += f"Ширина резонанса: {width:.3f} нм\n"
            response += f"Энергия: {energy:.3f} эВ\n"
            response += f"Частота: {frequency:.3f} ТГц\n"
            response += f"Волновое число: {wavenumber:.2f} см^-1"
            await message.answer_photo(buf)
            await message.reply(response)
            await ask_for_feedback(message, state, "resonance_position_and_width")
        except Exception as e:
            await message.reply("Ошибка при расчете резонанса. Пожалуйста, убедитесь, что файл содержит корректные данные.")
    else:
        await message.reply("Пожалуйста, отправьте файл в формате .txt или нажмите 'Отмена' для возврата в главное меню.")

@dp.message_handler(state=Form.waiting_for_spectrum_file)
async def process_invalid_spectrum_file(message: types.Message):
    await message.reply("Пожалуйста, отправьте файл в формате .txt или нажмите 'Отмена' для возврата в главное меню.")
@dp.message_handler(text="Другие")
async def physics_categories(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Механика"), KeyboardButton("Термодинамика"))
    keyboard.add(KeyboardButton("Электричество и магнетизм"), KeyboardButton("Оптика"))
    keyboard.add(KeyboardButton("Квантовая физика"), KeyboardButton("Ядерная физика"))
    keyboard.add(KeyboardButton("Волны"), KeyboardButton("Гидростатика"))
    keyboard.add(KeyboardButton("Специальная теория относительности"), KeyboardButton("Астрофизика"))
    keyboard.add(KeyboardButton("Назад"))
    await Form.waiting_for_physics_category.set()
    await message.reply("Выберите раздел физики:", reply_markup=keyboard)
@dp.message_handler(state=Form.waiting_for_physics_category)
async def process_physics_category(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
    else:
        await state.update_data(category=message.text)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

        if message.text == "Механика":
            keyboard.add("Сила", "Импульс", "Энергия-масса")
            keyboard.add("Работа", "Мощность", "Кинетическая энергия")
            keyboard.add("Потенциальная энергия")
        elif message.text == "Термодинамика":
            keyboard.add("Теплота", "Идеальный газ")
        elif message.text == "Электричество и магнетизм":
            keyboard.add("Электрическая сила", "Закон Ома", "Электрическая мощность")
            keyboard.add("Сила Лоренца")
        elif message.text == "Оптика":
            keyboard.add("Показатель преломления", "Тонкая линза")
        elif message.text == "Квантовая физика":
            keyboard.add("Энергия фотона", "Длина волны де Бройля")
        elif message.text == "Ядерная физика":
            keyboard.add("Радиоактивный распад")
        elif message.text == "Волны":
            keyboard.add("Скорость волны")
        elif message.text == "Гидростатика":
            keyboard.add("Гидростатическое давление", "Сила Архимеда")
        elif message.text == "Специальная теория относительности":
            keyboard.add("Замедление времени", "Сокращение длины")
        elif message.text == "Астрофизика":
            keyboard.add("Гравитационная сила")
        keyboard.add(KeyboardButton("Назад"))
        await Form.waiting_for_physics_calculation.set()
        await message.reply("Выберите физическую величину для расчета:", reply_markup=keyboard)
@dp.message_handler(state=Form.waiting_for_physics_calculation)
async def process_physics_calculation(message: types.Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Назад"))
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
    elif message.text == "Сила":
        await Form.waiting_for_force.set()
        await message.reply("Введите массу (кг) и ускорение (м/с²), разделенные пробелом.",reply_markup=keyboard)
    elif message.text == "Импульс":
        await Form.waiting_for_momentum.set()
        await message.reply("Введите массу (кг) и скорость (м/с), разделенные пробелом.",reply_markup=keyboard)
    elif message.text == "Энергия-масса":
        await Form.waiting_for_energy_mass.set()
        await message.reply("Введите массу (кг).",reply_markup=keyboard)
    elif message.text == "Работа":
        await Form.waiting_for_work.set()
        await message.reply("Введите силу (Н) и расстояние (м), разделенные пробелом.",reply_markup=keyboard)
    elif message.text == "Мощность":
        await Form.waiting_for_power.set()
        await message.reply("Введите работу (Дж) и время (с), разделенные пробелом.",reply_markup=keyboard)
    elif message.text == "Кинетическая энергия":
        await Form.waiting_for_kinetic_energy.set()
        await message.reply("Введите массу (кг) и скорость (м/с), разделенные пробелом.",reply_markup=keyboard)
    elif message.text == "Потенциальная энергия":
        await Form.waiting_for_potential_energy.set()
        await message.reply("Введите массу (кг), высоту (м) и ускорение свободного падения (м/с²), разделенные пробелом.",reply_markup=keyboard)
    elif message.text == "Теплота":
        await Form.waiting_for_heat.set()
        await message.reply("Введите массу (кг), удельную теплоемкость (Дж/(кг·К)) и изменение температуры (К), разделенные пробелом.",reply_markup=keyboard)
    elif message.text == "Идеальный газ":
        await Form.waiting_for_ideal_gas.set()
        await message.reply("Введите давление (Па), объем (м³), количество вещества (моль) и температуру (К), разделенные пробелом.",reply_markup=keyboard)
    elif message.text == "Электрическая сила":
        await Form.waiting_for_electric_force.set()
        await message.reply("Введите заряд (Кл) и напряженность электрического поля (Н/Кл), разделенные пробелом.",reply_markup=keyboard)
    elif message.text == "Закон Ома":
        await Form.waiting_for_ohms_law.set()
        await message.reply("Введите напряжение (В) и силу тока (А), разделенные пробелом.",reply_markup=keyboard)
    elif message.text == "Электрическая мощность":
        await Form.waiting_for_electric_power.set()
        await message.reply("Введите напряжение (В) и силу тока (А), разделенные пробелом.",reply_markup=keyboard)
    elif message.text == "Сила Лоренца":
        await Form.waiting_for_lorentz_force.set()
        await message.reply("Введите заряд (Кл), скорость (м/с) и магнитную индукцию (Тл), разделенные пробелом.",reply_markup=keyboard)
    elif message.text == "Показатель преломления":
        await Form.waiting_for_refractive_index.set()
        await message.reply("Введите скорость света в вакууме (м/с) и скорость света в среде (м/с), разделенные пробел ом.",reply_markup=keyboard)
    elif message.text == "Тонкая линза":
        await Form.waiting_for_thin_lens.set()
        await message.reply("Введите фокусное расстояние (м) и радиус кривизны (м), разделенные пробелом.",reply_markup=keyboard)
    elif message.text == "Энергия фотона":
        await Form.waiting_for_photon_energy.set()
        await message.reply("Введите частоту (Гц) или длину волны (м).",reply_markup=keyboard)
    elif message.text == "Де Бройля":
        await Form.waiting_for_de_broglie.set()
        await message.reply("Введите импульс (кг·м/с) или длину волны (м).",reply_markup=keyboard)
    elif message.text == "Радиоактивный распад":
        await Form.waiting_for_radioactive_decay.set()
        await message.reply("Введите начальное количество ядер (ядра) и время полураспада (с).",reply_markup=keyboard)
    elif message.text == "Скорость волны":
        await Form.waiting_for_wave_velocity.set()
        await message.reply("Введите частоту (Гц) и длину волны (м), разделенные пробелом.",reply_markup=keyboard)
    elif message.text == "Гидростатическое давление":
        await Form.waiting_for_hydrostatic_pressure.set()
        await message.reply("Введите глубину (м), плотность жидкости (кг/м³) и ускорение свободного падения (м/с²), разделенные пробелом.",reply_markup=keyboard)
    elif message.text == "Сила Архимеда":
        await Form.waiting_for_archimedes_force.set()
        await message.reply("Введите объем тела (м³), плотность жидкости (кг/м³) и ускорение свободного падения (м/с²), разделенные пробелом.",reply_markup=keyboard)
    elif message.text == "Дилатация времени":
        await Form.waiting_for_time_dilation.set()
        await message.reply("Введите скорость (м/с) и время в системе отсчета (с).",reply_markup=keyboard)
    elif message.text == "Сжатие длины":
        await Form.waiting_for_length_contraction.set()
        await message.reply("Введите скорость (м/с) и длину в системе отсчета (м).",reply_markup=keyboard)
    elif message.text == "Гравитационная сила":
        await Form.waiting_for_gravitational_force.set()
        await message.reply("Введите массу первого тела (кг), массу второго тела (кг) и расстояние между ними (м), разделенные пробелом.",reply_markup=keyboard)
    else:
        await message.reply("Неправильный выбор. Пожалуйста, выберите физическую операцию.")

@dp.message_handler(state=Form.waiting_for_force)
async def process_force(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        mass, acceleration = map(float, message.text.split())
        result = calculate_force(mass, acceleration)
        await message.reply(f"Сила равна {result} Н.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_momentum)
async def process_momentum(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        mass, velocity = map(float, message.text.split())
        result = calculate_momentum(mass, velocity)
        await message.reply(f"Импульс равен {result} кг·м/с.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_energy_mass)
async def process_energy_mass(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        mass = float(message.text)
        result = calculate_energy_mass_equivalence(mass)
        await message.reply(f"Энергия-масса равна {result} Дж.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")
    

@dp.message_handler(state=Form.waiting_for_work)
async def process_work(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        force, distance = map(float, message.text.split())
        result = calculate_work(force, distance)
        await message.reply(f"Работа равна {result} Дж.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")

@dp.message_handler(state=Form.waiting_for_power)
async def process_power(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        work, time = map(float, message.text.split())
        result = calculate_power(work, time)
        await message.reply(f"Мощность равна {result} Вт.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")

@dp.message_handler(state=Form.waiting_for_kinetic_energy)
async def process_kinetic_energy(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        mass, velocity = map(float, message.text.split())
        result = calculate_kinetic_energy(mass, velocity)
        await message.reply(f"Кинетическая энергия равна {result} Дж.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_potential_energy)
async def process_potential_energy(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        mass, height, g = map(float, message.text.split())
        result = calculate_potential_energy(mass, height, g)
        await message.reply(f"Потенциальная энергия равна {result} Дж.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_heat)
async def process_heat(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        mass, specific_heat , delta_temperature = map(float, message.text.split())
        result = calculate_heat(mass, specific_heat, delta_temperature)
        await message.reply(f"Теплота равна {result} Дж.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_ideal_gas)
async def process_ideal_gas(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        pressure, volume, n, temperature = map(float, message.text.split())
        result = ideal_gas_law(pressure, volume, n, temperature)
        await message.reply(f"Уравнение идеального газа: {result}.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_electric_force)
async def process_electric_force(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        charge, electric_field = map(float, message.text.split())
        result = electric_force(charge, electric_field)
        await message.reply(f"Электрическая сила равна {result} Н.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_ohms_law)
async def process_ohms_law(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        voltage, current = map(float, message.text.split())
        result = ohms_law(voltage, current)
        await message.reply(f"Сопротивление равно {result} Ом.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_electric_power)
async def process_electric_power(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        voltage, current = map(float, message.text.split())
        result = electric_power(voltage, current)
        await message.reply(f"Электрическая мощность равна {result} Вт.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_lorentz_force)
async def process_lorentz_force(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        charge, velocity, magnetic_field = map(float, message.text.split())
        result = lorentz_force(charge, velocity, magnetic_field)
        await message.reply(f"Сила Лоренца равна {result} Н.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_refractive_index)
async def process_refractive_index(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        c, v = map(float, message.text.split())
        result = refractive_index(c, v)
        await message.reply(f"Показатель преломления равен {result}.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_thin_lens)
async def process_thin_lens(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        f, u, v = map(float, message.text.split())
        result = thin_lens_equation(f, u, v)
        await message.reply(f"Уравнение тонкой линзы: {result}.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_photon_energy)
async def process_photon_energy(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        h, f = map(float, message.text.split())
        result = photon_energy(h, f)
        await message.reply(f"Энергия фотона равна {result} Дж.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_de_broglie)
async def process_de_broglie(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        h, p = map(float, message.text.split())
        result = de_broglie_wavelength(h, p)
        await message.reply(f"Длина волны де Бройля равна {result} м.")
    except ValueError:
        await message.reply("Неправиль ный формат ввода. Попробуйте еще раз.")
    await state.finish()

@dp.message_handler(state=Form.waiting_for_radioactive_decay)
async def process_radioactive_decay(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        N0, lambda_val, t = map(float, message.text.split())
        result = radioactive_decay(N0, lambda_val, t)
        await message.reply(f"Количество ядер равно {result}.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_wave_velocity)
async def process_wave_velocity(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        frequency, wavelength = map(float, message.text.split())
        result = wave_velocity(frequency, wavelength)
        await message.reply(f"Скорость волны равна {result} м/с.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_hydrostatic_pressure)
async def process_hydrostatic_pressure(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        rho, g, h = map(float, message.text.split())
        result = hydrostatic_pressure(rho, g, h)
        await message.reply(f"Гидростатическое давление равно {result} Па.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_archimedes_force)
async def process_archimedes_force(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        rho, V, g = map(float, message.text.split())
        result = archimedes_force(rho, V, g)
        await message.reply(f"Сила Архимеда равна {result} Н.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_time_dilation)
async def process_time_dilation(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        t, v, c = map(float, message.text.split())
        result = time_dilation(t, v, c)
        await message.reply(f"Замедление времени равно {result} с.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_length_contraction)
async def process_length_contraction(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        l, v, c = map(float, message.text.split())
        result = length_contraction(l, v, c)
        await message.reply(f"Сокращение длины равно {result} м.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")


@dp.message_handler(state=Form.waiting_for_gravitational_force)
async def process_gravitational_force(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.finish()
        await message.reply("Выберите операцию:", reply_markup=main_keyboard)
        return
    try:
        m1, m2, r = map(float, message.text.split())
        result = gravitational_force(m1, m2, r)
        await message.reply(f"Гравитационная сила равна {result} Н.")
        await ask_for_feedback(message, state, "other")
    except ValueError:
        await message.reply("Неправильный формат ввода. Попробуйте еще раз.")

if __name__ == '__main__':
    print('STARTING!')
    asyncio.run(dp.start_polling())