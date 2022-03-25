class Calculator():
    """
    """

    def calculate(self, output_data_path:str, show_plot:bool, output_plot_path:str):
        """
        """
        input_data = data_importer.get_input_data()
        conversion = data_calculator.calculate_conversion(input_data)
        selectivity = data_calculator.calculate_selectivity(input_data)
        self._print_results(conversion, selectivity)
        if output_data_path is not None:
            self._export_results(output_data_path, conversion, selectivity)
        if show_plot or output_plot_path is not None:
            plotter.plot(conversion, selectivity, show_plot, output_plot_path)
