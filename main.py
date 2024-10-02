import medical_data_visualizer
from unittest import main

# Testar as funções
medical_data_visualizer.draw_cat_plot()
medical_data_visualizer.draw_heat_map()

# Rodar os testes
main(module='test_module', exit=False)