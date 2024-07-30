# Calculadora de Menor Número de Passos

Este projeto é uma calculadora para encontrar a sequência de operações aritméticas que transforma um número inicial em um número alvo usando o menor número de passos possível. O programa utiliza uma interface gráfica criada com a biblioteca `customtkinter` e permite ao usuário definir um valor alvo e um número máximo de operações.

## Funcionalidades

- **Cálculo de Menor Número de Passos**: Calcula a menor sequência de operações para alcançar um valor alvo a partir de números de 1 até um número máximo fornecido pelo usuário.
- **Operações Permitidas**: `+`, `-`, `*`, `/`, `^` (potenciação).
- **Interface Gráfica**: Desenvolvida com `customtkinter` para uma experiência de usuário amigável.
- **Histórico de Cálculos**: Armazena e exibe o histórico de cálculos realizados, permitindo ao usuário visualizar e revisar cálculos anteriores.

## Estrutura do Código

- **Classes e Funções Principais**:
  - `QueueItem`: Representa um item na fila de prioridades, incluindo o valor atual, o número de passos, o operador utilizado e a lista de passos.
  - `f_value_evaluation(a, b, target)`: Avalia a função objetivo para comparar dois itens da fila.
  - `apply_operator(a, b, operator)`: Aplica um operador aritmético entre dois valores.
  - `skip_unnecessary_operators(value, current_value, operator, target)`: Determina se um operador deve ser ignorado com base no valor atual e no alvo.
  - `least_steps(target, max_src, allowed_operators)`: Encontra a menor sequência de passos para alcançar o valor alvo.
  - `run_calculation()`: Função chamada ao clicar no botão de cálculo; realiza o cálculo e atualiza a interface.
  - `save_to_history(target, max_src, steps)`: Salva o cálculo realizado no histórico.
  - `load_history()`: Carrega o histórico de cálculos a partir de um arquivo JSON.
  - `update_history_listbox()`: Atualiza a lista de histórico na interface gráfica.
  - `show_history_details(event)`: Exibe detalhes do cálculo selecionado no histórico.

- **Interface Gráfica**:
  - Utiliza `customtkinter` para criar a interface, incluindo campos de entrada, botão de cálculo, área para exibição dos resultados e lista de histórico.
  - A interface permite a entrada dos valores alvo e máximo, e exibe o resultado do cálculo e o histórico de cálculos.

## Requisitos

- `tkinter`: Biblioteca padrão para interfaces gráficas em Python.
- `customtkinter`: Biblioteca para personalização de interfaces tkinter.
- `json`: Biblioteca padrão para manipulação de dados JSON.
- `math`: Biblioteca padrão para funções matemáticas.

## Como Executar

1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
