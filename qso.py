import json
import random
import os

NUMBER_OF_FILES = 10  # Przykładowa liczba plików do wygenerowania
counter_21 = 0
counter_22 = 0
max_count = 2


if __name__ == '__main__':
    directory = 'qso_folder'

os.makedirs(directory, exist_ok=True)


def load_scenarios(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def load_and_choose_call_sign(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    call_signs = [item["Callsign"] for item in data]
    return random.choice(call_signs), call_signs

def generate_partial_sign(full_sign):
    sign_length = len(full_sign)
    if sign_length > 1:
        start_index = random.randint(0, sign_length - 2)
        end_index = random.randint(start_index + 1, sign_length)
        return full_sign[start_index:end_index]
    else:
        return full_sign
        


def process_stage(stage_number, stage_data, model_callsign, full_sign, partial_signs, last_partial_call, conversation, generated_report):

    action = stage_data['actions'][0]
    selected_option_key = random.choice(list(action['options'].keys()))

    # Zastępowanie znaków wywoławczych i raportów
    selected_option = selected_option_key.replace("{{model_callsign}}", model_callsign).replace("{{full_callsign}}", full_sign)

    # Obsługa raportu
    if "{{report}}" in selected_option:
        if not generated_report[0]:
            report_number = random.randint(1, 1999)
            generated_report[0] = "599 {:03d}".format(report_number) if report_number < 100 and random.choice([True, False]) else f"599 {report_number}"
        selected_option = selected_option.replace("{{report}}", generated_report[0])

    # Obsługa częściowego znaku wywoławczego
    if "{{partial_callsign}}" in selected_option:
        if not last_partial_call[0]:
            last_partial_call[0] = generate_partial_sign(full_sign)
        selected_option = selected_option.replace("{{partial_callsign}}", last_partial_call[0])

    # Obsługa omyłkowego uznania pełnego znaku za częściowy
    if "{{full_callsign_mistake}}" in selected_option:
        selected_option = selected_option.replace("{{full_callsign_mistake}}", full_sign)

    conversation.append({
        "stage_number": stage_number,  # Dodaj numer etapu tutaj
        "stage_type": stage_data['type'],
        "action": action['action'],
        "data": selected_option
    })


    next_stage = action['options'][selected_option_key]
    return next_stage



def traverse_scenario(scenario, model_callsign, full_sign, partial_signs, current_stage='1', max_count=3):
    conversation = []
    last_partial_call = [None]
    generated_report = [None]
    counter_21 = 0
    counter_22 = 0

    while current_stage:
        # Resetowanie liczników na początku nowej łączności
        if current_stage == '1':
            full_sign, partial_signs = load_and_choose_call_sign('cqww2022.json')
            counter_21 = 0
            counter_22 = 0
        
        # Przetwarzanie etapu i określanie następnego etapu
        stage_data = scenario[current_stage]
        next_stage = process_stage(current_stage, stage_data, model_callsign, full_sign, partial_signs, last_partial_call, conversation, generated_report)

        # Logika dla liczników
        if current_stage == '21':
            counter_21 += 1
            if counter_21 > max_count:
                next_stage = '40'
                counter_21 = 0  # Resetuj licznik
        elif current_stage == '22':
            counter_22 += 1
            if counter_22 > max_count:
                next_stage = '40'
                counter_22 = 0  # Resetuj licznik

        # Przechodzenie do następnego etapu
        if next_stage:
            current_stage = next_stage
        else:
            current_stage = '999'

        # Sprawdzanie końca scenariusza
        if current_stage not in scenario:
            if current_stage == '999':
                report = generated_report[0] if generated_report[0] else "59"
                conversation.append({
                    "stage": "output",
                    "action": "log",
                    "data": f"$LOG {full_sign} : {report}"
                })
            break

    return conversation




def main():
    model_callsign, _ = load_and_choose_call_sign('cqww2022.json')
    scenarios = load_scenarios('scenarios_qso.json')
    for i in range(NUMBER_OF_FILES):
        full_sign, partial_signs = load_and_choose_call_sign('cqww2022.json')
        partial_signs = [generate_partial_sign(full_sign) for _ in range(5)]

        for role, role_data in scenarios['roles'].items():
            conversation = traverse_scenario(role_data['stages'], model_callsign, full_sign, partial_signs)
            output = {
                "model_callsign": model_callsign,
                "role": role,
                "conversation": conversation,
                "status": {"full_callsign_received": True}
            }
            file_name = os.path.join(directory, f"qso_{i:05}.json")
            
            with open(file_name, 'w') as f:
                json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()




