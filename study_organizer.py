
import json

class StudyOrganizer:
    """
    Gerencia o cadastro de matérias e o tempo de estudo dedicado a cada uma.
    Os dados são persistidos em um arquivo JSON.
    """
    def __init__(self, data_file='study_data.json'):
        self.data_file = data_file
        self.data = self._load_data()

    def _load_data(self):
        """
        Carrega os dados de estudo do arquivo JSON. Se o arquivo não existir,
        retorna uma estrutura de dados vazia.
        """
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'subjects': {}}

    def _save_data(self):
        """
        Salva os dados de estudo no arquivo JSON.
        """
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_subject(self, subject_name):
        """
        Adiciona uma nova matéria se ela ainda não existir.
        Retorna True se a matéria foi adicionada, False caso contrário.
        """
        if subject_name not in self.data['subjects']:
            self.data['subjects'][subject_name] = {'study_time': 0}
            self._save_data()
            return True
        return False

    def record_study_time(self, subject_name, time_in_minutes):
        """
        Registra o tempo de estudo para uma matéria existente.
        Retorna True se o tempo foi registrado, False se a matéria não existe.
        """
        if subject_name in self.data['subjects']:
            self.data['subjects'][subject_name]['study_time'] += time_in_minutes
            self._save_data()
            return True
        return False

    def get_all_subjects(self):
        """
        Retorna um dicionário com todas as matérias e seus tempos de estudo.
        """
        return self.data['subjects']

    def get_subject_study_time(self, subject_name):
        """
        Retorna o tempo de estudo de uma matéria específica. Retorna 0 se a matéria não existe.
        """
        return self.data['subjects'].get(subject_name, {}).get('study_time', 0)

    def update_subject_name(self, old_name, new_name):
        """
        Atualiza o nome de uma matéria existente.
        Retorna True se o nome foi atualizado, False caso contrário (matéria antiga não existe ou nova já existe).
        """
        if old_name in self.data['subjects'] and new_name not in self.data['subjects']:
            self.data['subjects'][new_name] = self.data['subjects'].pop(old_name)
            self._save_data()
            return True
        return False

    def delete_subject(self, subject_name):
        """
        Exclui uma matéria existente.
        Retorna True se a matéria foi excluída, False se a matéria não existe.
        """
        if subject_name in self.data['subjects']:
            del self.data['subjects'][subject_name]
            self._save_data()
            return True
        return False


if __name__ == '__main__':
    # Exemplo de uso da classe StudyOrganizer
    organizer = StudyOrganizer()

    # Adicionar matérias
    print("\n--- Adicionando matérias ---")
    print(f"Adicionando Matemática Discreta: {organizer.add_subject('Matemática Discreta')}")
    print(f"Adicionando Programação Orientada a Objetos: {organizer.add_subject('Programação Orientada a Objetos')}")
    print(f"Adicionando Cálculo I: {organizer.add_subject('Cálculo I')}")
    print(f"Tentando adicionar Matemática Discreta novamente: {organizer.add_subject('Matemática Discreta')}")

    # Registrar tempo de estudo
    print("\n--- Registrando tempo de estudo ---")
    print(f"Registrando 60 min para Matemática Discreta: {organizer.record_study_time('Matemática Discreta', 60)}")
    print(f"Registrando 90 min para Programação Orientada a Objetos: {organizer.record_study_time('Programação Orientada a Objetos', 90)}")
    print(f"Registrando 30 min para Matemática Discreta: {organizer.record_study_time('Matemática Discreta', 30)}")
    print(f"Tentando registrar tempo para matéria inexistente: {organizer.record_study_time('Física I', 45)}")

    # Visualizar todas as matérias
    print("\n--- Matérias e tempos de estudo atuais ---")
    for subject, data in organizer.get_all_subjects().items():
        print(f'- {subject}: {data["study_time"]} minutos')

    # Editar nome de matéria
    print("\n--- Editando nome de matéria ---")
    print(f"Editando Cálculo I para Cálculo Diferencial e Integral I: {organizer.update_subject_name('Cálculo I', 'Cálculo Diferencial e Integral I')}")
    print(f"Tentando editar matéria inexistente: {organizer.update_subject_name('Física I', 'Física II')}")
    print(f"Tentando editar para nome já existente: {organizer.update_subject_name('Programação Orientada a Objetos', 'Cálculo Diferencial e Integral I')}")

    print("\n--- Matérias e tempos de estudo após edição ---")
    for subject, data in organizer.get_all_subjects().items():
        print(f'- {subject}: {data["study_time"]} minutos')

    # Excluir matéria
    print("\n--- Excluindo matéria ---")
    print(f"Excluindo Matemática Discreta: {organizer.delete_subject('Matemática Discreta')}")
    print(f"Tentando excluir matéria inexistente: {organizer.delete_subject('Física I')}")

    print("\n--- Matérias e tempos de estudo após exclusão ---")
    for subject, data in organizer.get_all_subjects().items():
        print(f'- {subject}: {data["study_time"]} minutos')



