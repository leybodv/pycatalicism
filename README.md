<h1>pycatalicism</h1>
<p>Program for control of catalytic activity of materials measurement equipment (to be developed...) as well as for calculation of main parameters relevant for catalyst functional properties characterization (conversion, activity, selectivity, stability, activation energy).</p>
<h2>Usage</h2>
<h3>Calculation of catalyst functional properties</h3>
<p>pycat calc --output-data OUTPUT_DATA --show-plot --output-plot OUPUT_PLOT input-data-path initial-data-path {co-oxidation|co2-hydrogenation}</p>
<p>positional arguments:</p>
<table>
  <tr>
    <td>input-data-path</td>
    <td>path to directory with files from concentration measurement device</td>
  </tr>
  <tr>
    <td>initial-data-path</td>
    <td>path to file with data of initial concentration measurement</td>
  </tr>
  <tr>
    <td>{co-oxidation|co2-hydrogenation}</td>
    <td>catalytic reaction for which to make calculations</td>
  </tr>
</table>
<p>parameters:</p>
<table>
  <tr>
    <td>--ouput-data OUPUT_DATA</td>
    <td>path to directory in which to export calculated data</td>
  </tr>
  <tr>
    <td>--show-plot</td>
    <td>if provided plot will be shown with calculated data</td>
  </tr>
  <tr>
    <td>--ouput-plot OUTPUT_PLOT</td>
    <td>path to directory in which to export plot of calclated data</td>
  </tr>
</table>
<br>
<p>To calculate conversion and selectivity for the reaction of interest program needs to know initial parameters, i.e. the ones before catalytic reaction started, and results of measurement at different temperatures of catalytic reaction. Minimal parameters are reaction participants concentrations in mol.% and temperatures of catalytic reaction. Parameters provided as files with strictly defined format:</p>
<br>
<p>
Температура&lt;tab&gt;<i>temperature</i><br>
&lt;br&gt;<br>
Название&lt;tab&gt;Время, мин&lt;tab&gt;Детектор&lt;tab&gt;Концентрация&lt;tab&gt;Ед, измерения&lt;tab&gt;Площадь&lt;tab&gt;Высота<br>
<i>compound-name</i>&lt;tab&gt;<i>retention-time</i>&lt;tab&gt;<i>detector-name</i>&lt;tab&gt;<i>compound-concentration</i>&lt;tab&gt;<i>concentration-units</i>&lt;tab&gt;<i>peak-area</i>&lt;tab&gt;<i>peak-height</i><br>
[&lt;br&gt;<br>
Темп. (газовые часы)&lt;tab&gt;<i>flow-temperature</i><br>
Давление (газовые часы)&lt;tab&gt;<i>flow-pressure</i><br>
Поток&lt;tab&gt;<i>flow-rate</i>]<br>
</p>
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
<h2>ToDo</h2>
<ul>
  <li>add docs</li>
  <li>implement abstract classes in "pythonic" way</li>
  <li>implement factory design in "pythonic" way?</li>
  <li>convert p, T, f data from gas clock to SI units before usage</li>
  <li>update calc/calc.py docs</li>
</ul>
