<h1>pycatalicism</h1>
<p>Program controls catalytic activity of materials measurement equipment (to be developed...) as well as calculates main parameters relevant for catalyst functional properties characterization (conversion, activity, selectivity, stability, activation energy).</p>
  <h2>Contents</h2>
  <ol>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#calc">Calculation of catalyst functional properties</a></li>
    <li><a href="#furnace-control">Furnace control</a></li>
    <li><a href="#chromatograph-control">Chromatograph control</a></li>
  </ol>
  <h2 id="installation">Installation</h2>
    <h3>Arch Linux</h3>
      <p>Install python:</p>
      <p><code>pacman -S python</code></p>
      <p>Install python libraries:</p>
      <p><code>pacman -S python-matplotlib python-numpy python-pyserial</code></p>
      <p><code>pip install pymodbus</code></p>
      <p>Install git:</p>
      <p><code>pacman -S git</code></p>
      <p>Clone repository (this will create pycatalicism directory inside your current directory):</p>
      <p><code>git clone https://github.com/leybodv/pycatalicism.git</code></p>
      <p>Create alias in your .bashrc file:</p>
      <p><code>pycat='PYTHONPATH="/path/to/pycatalicism-parent-directory" /path/to/pycat.py'</code></p>
    <h3>Windows</h3>
      <p>Install python from <a href="python.org">python.org</a></p>
      <p>Install python libraries (better to start cmd as administrator):</p>
      <p><code>pip install matplotlib numpy pyserial pymodbus</code></p>
      <p>Install git for windows from <a href="https://gitforwindows.org/">gitforwindows.org</a></p>
      <p>Clone repository in git bash:</p>
      <p><code>cd path/to/repository-storage-dir</code></p>
      <p><code>git clone https://github.com/leybodv/pycatalicism.git</code></p>
      <p>Add PYHTONPATH system variable with path/to/repository-storage-dir value</p>
      <p>Download and install driver for usb -> com from <a href="https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers">silabs.com</a></p>
  <h2 id="calc">Calculation of catalyst functional properties</h2>
    <p>NB: on Windows <code>pycat</code> must be replaced with <code>python path/to/pycat.py</code></p>
    <p><code>pycat calc --conversion|--selectivity [--output-data OUTPUT_DATA] [--show-plot] [--output-plot OUPUT_PLOT] [--products-basis] [--sample-name SAMPLE_NAME] input-data-path initial-data-path {co-oxidation|co2-hydrogenation}</code></p>
    <p>positional arguments:</p>
    <table>
      <tr>
        <td>input-data-path</td>
        <td>path to directory with files from concentration measurement device</td>
      </tr>
      <tr>
        <td>initial-data-path</td>
        <td>path to file with data of initial composition of gas</td>
      </tr>
      <tr>
        <td>{co-oxidation|co2-hydrogenation}</td>
        <td>reaction for which to calculate data</td>
      </tr>
    </table>
    <p>parameters:</p>
    <table>
      <tr>
        <td>--conversion|--selectivity</td>
        <td>whether to calculate conversion or selectivity for the specified reaction (at least one must be specified, can be specified both of them)</td>
      </tr>
      <tr>
        <td>--ouput-data OUPUT_DATA</td>
        <td>path to directory to save calculated data</td>
      </tr>
      <tr>
        <td>--show-plot</td>
        <td>whether to show data plot or not</td>
      </tr>
      <tr>
        <td>--ouput-plot OUTPUT_PLOT</td>
        <td>path to directory to save plot</td>
      </tr>
      <tr>
        <td>--products-basis</td>
        <td>calculate conversion based on products concentrations instead of reactants</td>
      </tr>
      <tr>
        <td>--sample-name</td>
        <td>sample name will be added to results data files and as a title to the resulting plots</td>
      </tr>
    </table>
    <br>
    <p>To calculate conversion and selectivity for the reaction of interest program needs to know initial parameters, i.e. the ones before catalytic reaction started, and results of measurement at different temperatures of catalytic reaction. Minimal parameters are reaction participants concentrations in mol.% and temperatures of catalytic reaction. Parameters are provided as files with strictly defined format:</p>
    <div><pre>
    Температура&lt;tab&gt;<i>temperature</i>
    &lt;br&gt;
    Название&lt;tab&gt;Время, мин&lt;tab&gt;Детектор&lt;tab&gt;Концентрация&lt;tab&gt;Ед, измерения&lt;tab&gt;Площадь&lt;tab&gt;Высота
    <i>compound-name</i>&lt;tab&gt;<i>retention-time</i>&lt;tab&gt;<i>detector-name</i>&lt;tab&gt;<i>compound-concentration</i>&lt;tab&gt;<i>concentration-units</i>&lt;tab&gt;<i>peak-area</i>&lt;tab&gt;<i>peak-height</i>
    [&lt;br&gt;
    Темп. (газовые часы)&lt;tab&gt;<i>flow-temperature</i>
    Давление (газовые часы)&lt;tab&gt;<i>flow-pressure</i>
    Поток&lt;tab&gt;<i>flow-rate</i>]
    </pre></div>
    <p>If program encounters file with wrong format, the file is ignored and corresponding warning is logged to console.</p>
    <table>
      <tr>
        <td><i>temperature</i></td>
        <td>temperature of catalytic reaction which will be used as X coordinate</td>
        <td>units does not matter, but expected to be the same for one series of experiment</td>
      </tr>
      <tr>
        <td><i>compound-name</i></td>
        <td>chemical formula of compound</td>
        <td rowspan="2">table with these parametes is simply copy-pasted from chromatec analytics software</td>
      </tr>
      <tr>
        <td><i>compound-concentraion</i></td>
        <td>concentration of compound in mol.%</td>
      </tr>
      <tr>
        <td><i>flow-temperature</i></td>
        <td>temperature at the point of gas total flow rate measurement in °C</td>
        <td rowspan="3">These parameters are optional and should be measured by means of gas clocks. If they are absent, program still will be able to calculate results, however, there will be error due to the change in reaction volume.</td>
      </tr>
      <tr>
        <td><i>flow-pressure</i></td>
        <td>pressure at the point of gas total flow rate measurement in Pa</td>
      </tr>
      <tr>
        <td><i>flow-rate</i></td>
        <td>gas total flow rate</td>
      </tr>
    </table>
    <p>Calculations are made using following equations:</p>
    <p><b>CO oxidation</b></p>
    <pre><img src="https://latex.codecogs.com/svg.image?\alpha&space;=&space;\frac{\frac{p_{i}\cdot&space;f_{i}}{T_{i}}\cdot&space;C_{CO,i}&space;-&space;\frac{p_f\cdot&space;f_f}{T_f}\cdot&space;C_{CO,f}}{\frac{p_{i}\cdot&space;f_{i}}{T_{i}}\cdot&space;C_{CO,i}}" title="https://latex.codecogs.com/svg.image?\alpha = \frac{\frac{p_{i}\cdot f_{i}}{T_{i}}\cdot C_{CO,i} - \frac{p_f\cdot f_f}{T_f}\cdot C_{CO,f}}{\frac{p_{i}\cdot f_{i}}{T_{i}}\cdot C_{CO,i}}" /></pre>
    <p>
      where<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;\alpha" title="https://latex.codecogs.com/svg.image?\inline \alpha" /> - CO conversion<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;C_{CO,i}" title="https://latex.codecogs.com/svg.image?\inline C_{CO,i}" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;C_{CO,f}" title="https://latex.codecogs.com/svg.image?\inline C_{CO,f}" /> - concentrations of CO before and after catalytic reactor, respectively, in mol.%<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;f_{i}" title="https://latex.codecogs.com/svg.image?\inline f_{i}" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;f_{f}" title="https://latex.codecogs.com/svg.image?\inline f_{f}" /> - total gas flow rates before and after catalytic reactor, respectively, in m<sup>3</sup>/s<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;p_i" title="https://latex.codecogs.com/svg.image?\inline p_i" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;p_f" title="https://latex.codecogs.com/svg.image?\inline p_f" /> - pressure of gas at point of total gas flow rate measurement before and after catalytic reactor, respectively, in Pa<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;T_i" title="https://latex.codecogs.com/svg.image?\inline T_i" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;T_f" title="https://latex.codecogs.com/svg.image?\inline T_f" /> - temperature of gas at point of total gas flow rate measurement before and after catalytic reactor, respectively, in K
    </p>
    <p><b>CO<sub>2</sub> hydrogenation</b></p>
    <pre><img src="https://latex.codecogs.com/svg.image?\inline&space;alpha&space;=&space;\frac{\frac{p_{i}\cdot&space;f_{i}}{T_{i}}\cdot&space;C_{CO_2,i}&space;-&space;\frac{p_f\cdot&space;f_f}{T_f}\cdot&space;C_{CO_2,f}}{\frac{p_{i}\cdot&space;f_{i}}{T_{i}}\cdot&space;C_{CO_2,i}}" title="https://latex.codecogs.com/svg.image?\inline alpha = \frac{\frac{p_{i}\cdot f_{i}}{T_{i}}\cdot C_{CO_2,i} - \frac{p_f\cdot f_f}{T_f}\cdot C_{CO_2,f}}{\frac{p_{i}\cdot f_{i}}{T_{i}}\cdot C_{CO_2,i}}" /></pre>
    <p>
      where<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;\alpha" title="https://latex.codecogs.com/svg.image?\inline \alpha" /> - CO<sub>2</sub> conversion<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;C_{CO_2,i}" title="https://latex.codecogs.com/svg.image?\inline C_{CO_2,i}" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;C_{CO_2,f}" title="https://latex.codecogs.com/svg.image?\inline C_{CO_2,f}" /> - concentrations of CO<sub>2</sub> before and after catalytic reactor, respectively, in mol.%<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;f_{i}" title="https://latex.codecogs.com/svg.image?\inline f_{i}" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;f_{f}" title="https://latex.codecogs.com/svg.image?\inline f_{f}" /> - total gas flow rates before and after catalytic reactor, respectively, in m<sup>3</sup>/s<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;p_i" title="https://latex.codecogs.com/svg.image?\inline p_i" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;p_f" title="https://latex.codecogs.com/svg.image?\inline p_f" /> - pressure of gas at point of total gas flow rate measurement before and after catalytic reactor, respectively, in Pa<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;T_i" title="https://latex.codecogs.com/svg.image?\inline T_i" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;T_f" title="https://latex.codecogs.com/svg.image?\inline T_f" /> - temperature of gas at point of total gas flow rate measurement before and after catalytic reactor, respectively, in K
    </p>
    <pre><img src="https://latex.codecogs.com/svg.image?\inline&space;S&space;=&space;\frac{n_i\cdot&space;C_i}{\sum&space;n_i\cdot&space;C_i}" title="https://latex.codecogs.com/svg.image?\inline S = \frac{n_i\cdot C_i}{\sum n_i\cdot C_i}" /></pre>
    <p>
      where<br>
      S - selectivity towards i<sup>th</sup> component<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;C_i" title="https://latex.codecogs.com/svg.image?\inline C_i" /> - concentration of i<sup>th</sup> component among CO, CH<sub>4</sub>, C<sub>2</sub>H<sub>6</sub>, C<sub>3</sub>H<sub>8</sub>, i-C<sub>4</sub>H<sub>10</sub>, n-C<sub>4</sub>H<sub>10</sub>, i-C<sub>5</sub>H<sub>12</sub>, n-C<sub>5</sub>H<sub>12</sub>, in mol.%<br>
      n - stoichiometry coefficient in CO<sub>2</sub> hydrogenation reaction (number of C atoms in product molecule)
    </p>
    <p><b>CO<sub>2</sub> hydrogenation, products basis</b></p>
    <p>Sometimes the results obtained with above equation give erroneous results with large negative conversions. It is useful to calculate CO<sub>2</sub> conversion based on products. However, this method is prone to error due to the assumption, that only certain products are formed.</p>
    <pre><img src="https://latex.codecogs.com/svg.image?\inline&space;\alpha&space;=&space;\frac{\sum{n_p\cdot&space;C_p}}{C_{CO_2,i}}\cdot&space;\frac{p_f&space;\cdot&space;f_f&space;\cdot&space;T_i}{p_i&space;\cdot&space;f_i&space;\cdot&space;T_f}" title="https://latex.codecogs.com/svg.image?\inline \alpha = \frac{\sum{n_p\cdot C_p}}{C_{CO_2,i}}\cdot \frac{p_f \cdot f_f \cdot T_i}{p_i \cdot f_i \cdot T_f}" /></pre>
    <p>
      where<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;C_{CO_2,i}" title="https://latex.codecogs.com/svg.image?\inline C_{CO_2,i}" /> - concentration of CO<sub>2</sub> before catalytic reactor, respectively, in mol.%<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;C_p" title="https://latex.codecogs.com/svg.image?\inline C_p" /> - concentrations of p<sup>th</sup> component among CO, CH<sub>4</sub>, C<sub>2</sub>H<sub>6</sub>, C<sub>3</sub>H<sub>8</sub>, i-C<sub>4</sub>H<sub>10</sub>, n-C<sub>4</sub>H<sub>10</sub>, i-C<sub>5</sub>H<sub>12</sub>, n-C<sub>5</sub>H<sub>12</sub>, in mol.%<br>
      n - stoichiometry coefficient in CO<sub>2</sub> hydrogenation reaction (number of C atoms in product molecule)<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;f_{i}" title="https://latex.codecogs.com/svg.image?\inline f_{i}" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;f_{f}" title="https://latex.codecogs.com/svg.image?\inline f_{f}" /> - total gas flow rates before and after catalytic reactor, respectively, in m<sup>3</sup>/s<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;p_i" title="https://latex.codecogs.com/svg.image?\inline p_i" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;p_f" title="https://latex.codecogs.com/svg.image?\inline p_f" /> - pressure of gas at point of total gas flow rate measurement before and after catalytic reactor, respectively, in Pa<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;T_i" title="https://latex.codecogs.com/svg.image?\inline T_i" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;T_f" title="https://latex.codecogs.com/svg.image?\inline T_f" /> - temperature of gas at point of total gas flow rate measurement before and after catalytic reactor, respectively, in K
    </p>
    <p>If flow rate measurement data is not provided, conversion is calculated based solely on concentrations and warning is logged to console in this case.</p>
  <h2 id="furnace-control">Furnace control</h2>
    <p><code>pycat heat [--wait WAIT] [--show-plot] [--export-plot EXPORT_PLOT] [--export-data EXPORT_DATA] temperature</code></p>
    <p>positional arguments:</p>
    <p>
      <table>
        <tr>
          <td>temperature</td>
          <td>temperature in °C to heat furnace to. If 0, sets set point of a controller to 0 and turns off temperature regulation</td>
        </tr>
      </table>
    </p>
    <p>parameters:</p>
      <table>
        <tr>
          <td>--wait WAIT</td>
          <td>wait for WAIT minutes after a furnace has reached target temperature and turn heating off afterwards</td>
        </tr>
        <tr>
          <td>--show-plot</td>
          <td>show plot of temperature vs. time. NB: this will block the program until the window with the plot is closed</td>
        </tr>
        <tr>
          <td>--export-plot EXPORT_PLOT</td>
          <td>export temperature vs. time plot to the file specified by EXPORT_PLOT path</td>
        </tr>
        <tr>
          <td>--export-data</td>
          <td>export temperature vs. time data to the file specified by EXPORT_DATA path</td>
        </tr>
      </table>
      <p>Program should be configured prior use. The configuration file located in path/to/pycatalycism/furnace/furnace_config.py</p>
    <h2 id="chromatograph-control">Chromatograph control</h2>
    <p>Chromatec Crystal 5000 chromatograph can be controled via modbus protocol. The protocol requires modbus server to be run. Chromatec Control Panel and Chromatec Analytic with special module from chromatec installation media surve as modbus server (see chromatec documentation for details). Before using this python program, modbus server must be configured at Control Panel and Analytic software and relevant holding and input registers must be added. For the list of required registers see config.py file at the root of pycatalycism package.</p>
    <p><b>Commands:</b></p>
    <p><code>pycat chromatograph connect</code></p>
    <p>Opens Control Panel. Connection to chromatograph is istablished automatically. Analytic software is also automatically opened. Program waits for succsessful connection establishment, so, if chromatograph is not on, program will be hang forever.</p>
    <p><code>pycat chromatograph set-method method</code></p>
    <p>Sets instrumental method to the specified one and starts preparation to analysis step. The list of methods must be in a config.py file.</p>
    <p>positional arguments:</p>
    <p>
      <table>
        <tr>
          <td>method</td>
          <td>instrumental method</td>
        </tr>
      </table>
    </p>
    <p><code>pycat chromatograph start-analysis</code></p>
    <p>Starts measurement.</p>
    <p><code>pycat chromatograph set-passport --name NAME [--volume VOL] [--dilution DIL] [--purpose {analysis|graduation}] --operator OP --column COL [--lab-name LN]</code></p>
    <p>Set parameters to a passport of chromatogram. This method should be run only after the analysis step is over and before next analysis is started.</p>
    <p>required parameters:</p>
    <p>
      <table>
        <tr>
          <td>--name NAME</td>
          <td>name of chromatogram</td>
        </tr>
        <tr>
          <td>--operator OP</td>
          <td>name of operator</td>
        </tr>
        <tr>
          <td>--column COL</td>
          <td>name of column</td>
        </tr>
      </table>
    </p>
    <p>optional parameters:</p>
    <p>
      <table>
        <tr>
          <td>--volume VOL</td>
          <td>sample's volume, 0.5 by default</td>
        </tr>
        <tr>
          <td>--dilution DIL</td>
          <td>sample's dilution, 1 by default</td>
        </tr>
        <tr>
          <td>--purpose {analysis|graduation}</td>
          <td>purpose of chromatogram, analysis by default</td>
        </tr>
        <tr>
          <td>--lab-name LN</td>
          <td>name of lab, Inorganic Nanomaterials by default</td>
        </tr>
      </table>
    </p>
  <h2>ToDo</h2>
    <ul>
      <li>add mass flow controllers package</li>
      <li>rewrite calc module. Selectivity should be calculated automatically if applicable. There should be two separate commands to calculate activity and conversion</li>
      <li>add furnace read temperature interface</li>
      <li>convert p, T, f data from gas clock to SI units before usage</li>
    </ul>
