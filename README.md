<h1>pycatalicism</h1>
<p>Программа для контроля оборудования для измерения каталитических характеристик материалов в проточном режиме в реакциях окисления CO и гидрирования CO<sub>2</sub> с образованием CO и алканов до пентана. Оборудование состоит из 3х регуляторов расхода газа, печи и хроматографа. Контроль температуры печи осуществляется с помощью ПИД регулятора. Также с помощью программы можно проводить рассчёт основных параметров: конверсии (степени превращения) каталитической реакции, активности и селективности.</p>
  <h2>Содержание</h2>
  <ol>
    <li><a href="#installation">Установка программы</a></li>
    <li><a href="#calc">Рассчёт параметров</a></li>
    <li><a href="#furnace-control">Управление печи</a></li>
    <li><a href="#chromatograph-control">Управление хроматографом</a></li>
    <li><a href="#mfc">Управление регуляторами расхода газов</a></li>
  </ol>
  <h2 id="installation">Установка программы</h2>
    <h3>Arch Linux</h3>
      <p>Установить python:</p>
      <p><code>pacman -S python</code></p>
      <p>Установить библиотеки:</p>
      <p><code>pacman -S python-matplotlib python-numpy python-pyserial</code></p>
      <p><code>pip install pymodbus bronkhorst-propar</code></p>
      <p>Установить git:</p>
      <p><code>pacman -S git</code></p>
      <p>Клонировать репозиторий (будет создана папка pycatalicism в папке, в которой запущена команда):</p>
      <p><code>git clone https://github.com/leybodv/pycatalicism.git</code></p>
      <p>Создать alias в файле .bashrc:</p>
      <p><code>pycat='PYTHONPATH="/path/to/pycatalicism-parent-directory" /path/to/pycat.py'</code></p>
    <h3>Windows</h3>
      <p>Установить python отсюда: <a href="python.org">python.org</a></p>
      <p>Установить библиотеки:</p>
      <p><code>pip install matplotlib numpy pyserial pymodbus bronkhorst-propar</code></p>
      <p>Установить git для Windows: <a href="https://gitforwindows.org/">gitforwindows.org</a></p>
      <p>Клонировать репозиторий в git bash:</p>
      <p><code>cd path/to/repository-storage-dir</code></p>
      <p><code>git clone https://github.com/leybodv/pycatalicism.git</code></p>
      <p>Добавить переменную среды PYTHONPATH со значением path/to/repository-storage-dir</p>
      <p>Скачать и установить драйвер usb -> com отсюда: <a href="https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers">silabs.com</a></p>
  <h2 id="calc">Рассчёт характеристик катализаторов</h2>
    <p>NB: в Windows <code>pycat</code> нужно заменить на <code>python path/to/pycat.py</code></p>
    <p><code>pycat calc --conversion|--selectivity [--output-data OUTPUT_DATA] [--show-plot] [--output-plot OUPUT_PLOT] [--products-basis] [--sample-name SAMPLE_NAME] input-data-path initial-data-path {co-oxidation|co2-hydrogenation}</code></p>
    <p>Аргументы:</p>
    <table>
      <tr>
        <td>input-data-path</td>
        <td>путь к папке с файлами, содержащими данные о концентрациях компонентов реакции, температуре и потоках газов</td>
      </tr>
      <tr>
        <td>initial-data-path</td>
        <td>путь к файлу с данными о начальной концентрации компонентов реакции</td>
      </tr>
      <tr>
        <td>{co-oxidation|co2-hydrogenation}</td>
        <td>реакция, для которой провести рассчёт</td>
      </tr>
    </table>
    <p>Флаги:</p>
    <table>
      <tr>
        <td>--conversion|--selectivity</td>
        <td>следует ли провести рассчёт конверсии и/или селективности (по крайней мере один из вариантов должен быть указан)</td>
      </tr>
      <tr>
        <td>--ouput-data OUPUT_DATA</td>
        <td>путь к папке, в которую сохранить результаты рассчёта</td>
      </tr>
      <tr>
        <td>--show-plot</td>
        <td>показать график зависимости конверсии/селективности от температуры</td>
      </tr>
      <tr>
        <td>--ouput-plot OUTPUT_PLOT</td>
        <td>путь к папке, в которую сохранить график зависимости конверсии/селективности</td>
      </tr>
      <tr>
        <td>--products-basis</td>
        <td>рассчитать конверсию из данных о концентрации продуктов, вместо исходных компонентов</td>
      </tr>
      <tr>
        <td>--sample-name</td>
        <td>id образца будет добавлено в файл с результатами рассчёта, а также на график</td>
      </tr>
    </table>
    <br>
    <p>Для рассчёта конверсии и селективности программе необходимо знать исходные параметры, измеренные на входе в реактор, и параметры на выходе из реактора, полученные в результате измерения при различных температурах реакции. Минимальные параметры для рассчёта: концентрации компонентов реакции в мол.% и температуры, при которых проводились измерения. Данные для рассчёта должны сохраняться в файлах в определённом формате:</p>
    <div><pre>
    Температура&lt;tab&gt;<i>temperature</i>
    &lt;br&gt;
    Название&lt;tab&gt;Концентрация
    <i>compound-name</i>&lt;tab&gt;<i>compound-concentration</i>
    [&lt;br&gt;
    Темп. (газовые часы)&lt;tab&gt;<i>flow-temperature</i>
    Давление (газовые часы)&lt;tab&gt;<i>flow-pressure</i>
    Поток&lt;tab&gt;<i>flow-rate</i>]
    </pre></div>
    <p>Если файл содержит данные в неверном формате, такой файл игнорируется, а соответствующее сообщение выводится в консоль.</p>
    <table>
      <tr>
        <td><i>temperature</i></td>
        <td>температура, при которой проводилось измерение концентраций и которая будет использоваться в качестве данных оси абсцисс для построения графиков</td>
        <td></td>
      </tr>
      <tr>
        <td><i>compound-name</i></td>
        <td>название компонента реакции</td>
        <td rowspan="2">эта таблица получается копированием данных результатов рассчётов из программы Хроматэк Аналитик. Помимо этих данных в таблице также могут присутствовать столбцы других значений (напр. высота пика, площадь и т.п.), что не влияет на конечный результат</td>
      </tr>
      <tr>
        <td><i>compound-concentraion</i></td>
        <td>концентрация компонента в мол.%</td>
      </tr>
      <tr>
        <td><i>flow-temperature</i></td>
        <td>температура в точке измерения общего потока газов в °C</td>
        <td rowspan="3">Данные параметры должны быть измерены с помощью газовых часов на выходе из реактора. Эти параметры не являются необходимыми для рассчёта характеристик катализатора. Если они не будут указаны в файле, параметры всё равно будут рассчитаны, однако, в результатах будет ошибка, связанная с изменением объёма реагентов.</td>
      </tr>
      <tr>
        <td><i>flow-pressure</i></td>
        <td>давление в точке измерения общего потока газов в Па</td>
      </tr>
      <tr>
        <td><i>flow-rate</i></td>
        <td>общий поток газов в мл/мин</td>
      </tr>
    </table>
    <p>Рассчёты проводятся с использованием следующих уравнений:</p>
    <p><b>Окисление CO</b></p>
    <pre><img src="https://latex.codecogs.com/svg.image?\alpha&space;=&space;\frac{\frac{p_{i}\cdot&space;f_{i}}{T_{i}}\cdot&space;C_{CO,i}&space;-&space;\frac{p_f\cdot&space;f_f}{T_f}\cdot&space;C_{CO,f}}{\frac{p_{i}\cdot&space;f_{i}}{T_{i}}\cdot&space;C_{CO,i}}" title="https://latex.codecogs.com/svg.image?\alpha = \frac{\frac{p_{i}\cdot f_{i}}{T_{i}}\cdot C_{CO,i} - \frac{p_f\cdot f_f}{T_f}\cdot C_{CO,f}}{\frac{p_{i}\cdot f_{i}}{T_{i}}\cdot C_{CO,i}}" /></pre>
    <p>
      где<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;\alpha" title="https://latex.codecogs.com/svg.image?\inline \alpha" /> - конверсия CO<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;C_{CO,i}" title="https://latex.codecogs.com/svg.image?\inline C_{CO,i}" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;C_{CO,f}" title="https://latex.codecogs.com/svg.image?\inline C_{CO,f}" /> - концентрации CO до и после каталитического реактора, соответственно, в мол.%<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;f_{i}" title="https://latex.codecogs.com/svg.image?\inline f_{i}" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;f_{f}" title="https://latex.codecogs.com/svg.image?\inline f_{f}" /> - общий поток газов до и после каталитического реактора, соответственно, в м<sup>3</sup>/с<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;p_i" title="https://latex.codecogs.com/svg.image?\inline p_i" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;p_f" title="https://latex.codecogs.com/svg.image?\inline p_f" /> - давление в точке измерения общего потока газов до и после каталитического реактора, соответственно, в Па<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;T_i" title="https://latex.codecogs.com/svg.image?\inline T_i" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;T_f" title="https://latex.codecogs.com/svg.image?\inline T_f" /> - температура в точке измерения общего потока газов до и после каталитического реактора, соответственно, в К
    </p>
    <p><b>Гидрирование CO<sub>2</sub></b></p>
    <pre><img src="https://latex.codecogs.com/svg.image?\inline&space;alpha&space;=&space;\frac{\frac{p_{i}\cdot&space;f_{i}}{T_{i}}\cdot&space;C_{CO_2,i}&space;-&space;\frac{p_f\cdot&space;f_f}{T_f}\cdot&space;C_{CO_2,f}}{\frac{p_{i}\cdot&space;f_{i}}{T_{i}}\cdot&space;C_{CO_2,i}}" title="https://latex.codecogs.com/svg.image?\inline alpha = \frac{\frac{p_{i}\cdot f_{i}}{T_{i}}\cdot C_{CO_2,i} - \frac{p_f\cdot f_f}{T_f}\cdot C_{CO_2,f}}{\frac{p_{i}\cdot f_{i}}{T_{i}}\cdot C_{CO_2,i}}" /></pre>
    <p>
      где<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;\alpha" title="https://latex.codecogs.com/svg.image?\inline \alpha" /> - конверсия CO<sub>2</sub><br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;C_{CO_2,i}" title="https://latex.codecogs.com/svg.image?\inline C_{CO_2,i}" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;C_{CO_2,f}" title="https://latex.codecogs.com/svg.image?\inline C_{CO_2,f}" /> - концентрации CO<sub>2</sub> до и после каталитического реактора, соответственно, в мол.%<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;f_{i}" title="https://latex.codecogs.com/svg.image?\inline f_{i}" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;f_{f}" title="https://latex.codecogs.com/svg.image?\inline f_{f}" /> - общий поток газов до и после каталитического реактора, соответственно, в м<sup>3</sup>/с<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;p_i" title="https://latex.codecogs.com/svg.image?\inline p_i" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;p_f" title="https://latex.codecogs.com/svg.image?\inline p_f" /> - давление газа в точке измерения общего потока газов до и после каталитического реактора, соответственно, в Па<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;T_i" title="https://latex.codecogs.com/svg.image?\inline T_i" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;T_f" title="https://latex.codecogs.com/svg.image?\inline T_f" /> - температура газа в точке измерения общего потока газов до и после каталитического реактора, соответственно, в К
    </p>
    <pre><img src="https://latex.codecogs.com/svg.image?\inline&space;S&space;=&space;\frac{n_i\cdot&space;C_i}{\sum&space;n_i\cdot&space;C_i}" title="https://latex.codecogs.com/svg.image?\inline S = \frac{n_i\cdot C_i}{\sum n_i\cdot C_i}" /></pre>
    <p>
      где<br>
      S - селективность по отношению компонента i<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;C_i" title="https://latex.codecogs.com/svg.image?\inline C_i" /> - концентрация компонента i (CO, CH<sub>4</sub>, C<sub>2</sub>H<sub>6</sub>, C<sub>3</sub>H<sub>8</sub>, i-C<sub>4</sub>H<sub>10</sub>, n-C<sub>4</sub>H<sub>10</sub>, i-C<sub>5</sub>H<sub>12</sub>, n-C<sub>5</sub>H<sub>12</sub>), в мол.%<br>
      n - стехиометрический коэффициент в реакции гидрирования CO<sub>2</sub> (количество атомов C в молекуле продукта)
    </p>
    <p><b>гидрирование CO<sub>2</sub>, рассчёт на основе продуктов реакции</b></p>
    <p>Данный метод может быть использован для рассчёта конверсии углекислого газа, однако, результат может содержать ошибку, связанную с предположением, что только использованные для рассчёта компоненты образовались в результате реакции.</p>
    <pre><img src="https://latex.codecogs.com/svg.image?\inline&space;\alpha&space;=&space;\frac{\sum{n_p\cdot&space;C_p}}{C_{CO_2,i}}\cdot&space;\frac{p_f&space;\cdot&space;f_f&space;\cdot&space;T_i}{p_i&space;\cdot&space;f_i&space;\cdot&space;T_f}" title="https://latex.codecogs.com/svg.image?\inline \alpha = \frac{\sum{n_p\cdot C_p}}{C_{CO_2,i}}\cdot \frac{p_f \cdot f_f \cdot T_i}{p_i \cdot f_i \cdot T_f}" /></pre>
    <p>
      где<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;C_{CO_2,i}" title="https://latex.codecogs.com/svg.image?\inline C_{CO_2,i}" /> - концентрация CO<sub>2</sub> до каталитического реактора в мол.%<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;C_p" title="https://latex.codecogs.com/svg.image?\inline C_p" /> - концентрации компонента p (CO, CH<sub>4</sub>, C<sub>2</sub>H<sub>6</sub>, C<sub>3</sub>H<sub>8</sub>, i-C<sub>4</sub>H<sub>10</sub>, n-C<sub>4</sub>H<sub>10</sub>, i-C<sub>5</sub>H<sub>12</sub>, n-C<sub>5</sub>H<sub>12</sub>), в мол.%<br>
      n - стехиометрический коэффициент в реакции гидрирования CO<sub>2</sub> (количество атомов C в молекуле продукта)<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;f_{i}" title="https://latex.codecogs.com/svg.image?\inline f_{i}" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;f_{f}" title="https://latex.codecogs.com/svg.image?\inline f_{f}" /> - общий поток газов до и после каталитического реактора, соответственно, в м<sup>3</sup>/с<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;p_i" title="https://latex.codecogs.com/svg.image?\inline p_i" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;p_f" title="https://latex.codecogs.com/svg.image?\inline p_f" /> - давление газа в точке измерения общего потока газа до и после каталитического реактора, соответственно, в Па<br>
      <img src="https://latex.codecogs.com/svg.image?\inline&space;T_i" title="https://latex.codecogs.com/svg.image?\inline T_i" />, <img src="https://latex.codecogs.com/svg.image?\inline&space;T_f" title="https://latex.codecogs.com/svg.image?\inline T_f" /> - температура газа в точке измерения общего потока газа до и после каталитического реактора, соответственно, в К
    </p>
    <p>В случае, если данные об измерении общего потока газа не были измерены, конверсия рассчитывается только на основе данных о концентрациях, а в консоль выводится предупреждение.</p>
  <h2 id="furnace-control">Контроль печи</h2>
  <p>Контроль печи осуществляется с помощью контроллера ОВЕН ТРМ101, связь с которым устанавливается через последовательный порт. Параметры конфигурации контроллера должны быть прописаны в файле <a href="https://github.com/leybodv/pycatalicism/blob/dev/config.py">config.py</a></p>
    <p><code>pycat furnace set-temperature temperature</code></p>
    <p>Устанавить значение параметра SP регулятора.</p>
    <p>Аргументы:</p>
    <p>
      <table>
        <tr>
          <td>temperature</td>
          <td>Температура в °C</td>
        </tr>
      </table>
    </p>
    <p><code>pycat furnace print-temperature</code></p>
    <p>Вывести измеренную температуру в консоль.</p>
  <h2 id="chromatograph-control">Управление хроматографом</h2>
    <p>Осуществляется управление хроматографом Хроматэк Кристалл 5000 через протокол Modbus. Для работы протокола необходимо, чтобы был запущен сервер Modbus, в качестве которых выступают Панель управления и Аналитик, а также специальная программа, которую необходимо установить с установочного диска ПО Хроматэк (см. документацию Modbus из комплекта документации Хроматэк для более детальной инструкции). Перед работой с pycatalytic, необходимо добавить нужные регистры Modbus в Панели управления и Аналитик. Список необходимых регистров прописывается в конфигурации программы и может быть найден здесь: <a href="https://github.com/leybodv/pycatalicism/blob/dev/config.py">config.py</a></p>
    <p><b>Доступные комманды:</b></p>
    <p><code>pycat chromatograph set-method method</code></p>
    <p>Sets instrumental method to the specified one and starts preparation to analysis step. The list of methods must be in a <a href="https://github.com/leybodv/pycatalicism/blob/dev/config.py">config.py</a> file. If chromatec Control Panel or Analytic are not ON, starts these programs and connects to chromatograph. In this case, program waits for successful connection establishment, so, if chromatograph is not on, program will be hang forever.</p>
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
  <h2 id="mfc">Mass flow controllers</h2>
  <p>Program controls Bronkhorst F201CV mass flow controllers to control flow rates of He, CO2, O2, H2, CO or CH4 gases. Parameters of corresponding mass flow controllers must be added to <a href="https://github.com/leybodv/pycatalicism/blob/dev/config.py">config.py</a> file.</p>
  <p><code>pycat mfc set-flow-rate --gas {He|CO2|O2|H2|CO|CH4} --flow-rate FR</code></p>
  <p>Set gas flow rate to specified value in nml/min</p>
  <p>
    <table>
      <tr>
        <td>--gas {He|CO2|O2|H2|CO|CH4}</td>
        <td>gas to set flow rate for. Program chooses mass flow controller based on this value</td>
      </tr>
      <tr>
        <td>--flow-rate FR</td>
        <td>Flow rate in nml/min</td>
      </tr>
    </table>
  </p>
  <p><code>pycat mfc set-calibration --gas {He|CO2|O2|H2|CO|CH4} --calibration-number CN</code></p>
  <p>Set calibration of specified mass flow controller to the calibration number CN</p>
  <p>
    <table>
      <tr>
        <td>--gas {He|CO2|O2|H2|CO|CH4}</td>
        <td>Gas to set calibration for. Program chooses mass flow controller based on this value.</td>
      </tr>
      <tr>
        <td>--calibration-number CN</td>
        <td>Calibration number which can be found in the documentaion supplied with mass flow controller</td>
      </tr>
    </table>
  </p>
  <p><code>pycat mfc print-flow-rate --gas {He|CO2|O2|H2|CO|CH4}</code></p>
  <p>Print current flow rate in nml/min for specified gas.</p>
  <p>
    <table>
      <tr>
        <td>--gas {He|CO2|O2|H2|CO|CH4}</td>
        <td>Gas to print current flow rate for. Program chooses mass flow controller based on this value.</td>
      </tr>
    </table>
  </p>
  <h2>ToDo</h2>
    <ul>
      <li>write co_oxidation.py script</li>
      <li>rewrite calc module. Selectivity should be calculated automatically if applicable. There should be two separate commands to calculate activity and conversion</li>
      <li>add furnace read temperature interface</li>
      <li>convert p, T, f data from gas clock to SI units before usage</li>
    </ul>
