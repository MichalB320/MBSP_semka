import random

# Parametre simulácie
NUM_DOCTORS = 4
SHIFT_HOURS = 6
ACUTE_CASES_PER_DAY = (6, 10)
TREATMENT_TIME_NORMAL = (20, 30)
TREATMENT_TIME_COMPLEX = (40, 60)
COMPLEX_CASE_PROB = 0.2
APPOINTMENT_VARIATION = (-10, 10)
END_TIME = SHIFT_HOURS * 60  # Čas v minútach
REPLICATIONS = 700  # Počet replikácií simulácie

# Trieda pacienta
class Patient:
    def __init__(self, arrival_time, urgent=False):
        self.arrival_time = arrival_time
        self.urgent = urgent
        self.treatment_time = random.randint(*TREATMENT_TIME_COMPLEX) if random.random() < COMPLEX_CASE_PROB else random.randint(*TREATMENT_TIME_NORMAL)

# Funkcia simulácie
def simulate_clinic():
    event_list = []
    doctors_available = NUM_DOCTORS
    waiting_queue = []
    total_waiting_time = 0
    treated_patients = 0

    # Generovanie pacientov
    appointment_times = [random.randint(0, END_TIME) + random.randint(*APPOINTMENT_VARIATION) for _ in range(30)]
    acute_cases = [random.randint(0, END_TIME) for _ in range(random.randint(*ACUTE_CASES_PER_DAY))]

    for time in appointment_times:
        event_list.append(("arrival", time, Patient(time)))

    for time in acute_cases:
        event_list.append(("arrival", time, Patient(time, urgent=True)))

    # Zoradenie udalostí podľa času
    event_list.sort(key=lambda x: x[1])

    current_time = 0
    while event_list:
        event_type, event_time, patient = event_list.pop(0)
        current_time = event_time

        if event_type == "arrival":
            if doctors_available > 0:
                doctors_available -= 1
                event_list.append(("release_doctor", current_time + patient.treatment_time, None))
                event_list.sort(key=lambda x: x[1])
            else:
                waiting_queue.append(patient)

        elif event_type == "release_doctor":
            doctors_available += 1
            if waiting_queue:
                p = waiting_queue.pop(0)
                waiting_time = current_time - p.arrival_time
                total_waiting_time += waiting_time
                treated_patients += 1
                doctors_available -= 1
                event_list.append(("release_doctor", current_time + p.treatment_time, None))
                event_list.sort(key=lambda x: x[1])

    avg_waiting_time = total_waiting_time / max(1, treated_patients)
    return avg_waiting_time

# Spustenie replikácií simulácie
results = []
for _ in range(REPLICATIONS):
    results.append(simulate_clinic())

average_waiting_time = sum(results) / len(results)

print(f"Priemerný čas čakania po {REPLICATIONS} replikáciách: {average_waiting_time:.2f} minút")