<h1>pycatalicism</h1>
<p>Программа для контроля оборудования для измерения каталитических характеристик материалов в проточном режиме в реакциях окисления CO и гидрирования CO<sub>2</sub> с образованием CO и алканов до пентана. Оборудование состоит из 3х регуляторов расхода газа, печи и хроматографа. Контроль температуры печи осуществляется с помощью ПИД регулятора. Также с помощью программы можно проводить расчёт основных параметров: конверсии (степени превращения) каталитической реакции, активности и селективности.</p>
  <h2>Содержание</h2>
  <ol>
    <li><a href="#installation">Установка программы</a></li>
    <li><a href="#calc">Рассчёт параметров</a></li>
    <li><a href="#furnace-control">Управление печи</a></li>
    <li><a href="#chromatograph-control">Управление хроматографом</a></li>
    <li><a href="#mfc">Управление регуляторами расхода газов</a></li>
    <li><a href="#valves">Управление соленоидными клапанами</a></li>
    <li><a href="#activation">Проведение активации</a></li>
    <li><a href="#measurement">Проведение измерения</a></li>
    <li><a href="#init-conc-measurement">Проведение измерения исходной концентрации реагентов</a></li>
  </ol>
  <h2 id="installation">Установка программы</h2>
    <h3>Arch Linux</h3>
      <p>Установить python:</p>
      <p><code>pacman -S python</code></p>
      <p>Установить программу:</p>
      <p><code>pip install pycatalicism</code></p>
    <h3>Windows</h3>
      <p>Установить python отсюда: <a href="python.org">python.org</a></p>
      <p>Установить программу:</p>
      <p><code>pip install pycatalicism</code></p>
      <p>Скачать и установить драйвер usb -> com отсюда: <a href="https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers">silabs.com</a></p>
  <h2 id="calc">Рассчёт характеристик катализаторов</h2>
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
        <td>реакция, для которой провести расчёт</td>
      </tr>
    </table>
    <p>Флаги:</p>
    <table>
      <tr>
        <td>--conversion|--selectivity</td>
        <td>следует ли провести расчёт конверсии и/или селективности (по крайней мере один из вариантов должен быть указан)</td>
      </tr>
      <tr>
        <td>--ouput-data OUPUT_DATA</td>
        <td>путь к папке, в которую сохранить результаты расчёта</td>
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
        <td>id образца будет добавлено в файл с результатами расчёта, а также на график</td>
      </tr>
    </table>
    <br>
    <p>Для расчёта конверсии и селективности программе необходимо знать исходные параметры, измеренные на входе в реактор, и параметры на выходе из реактора, полученные в результате измерения при различных температурах реакции. Минимальные параметры для расчёта: концентрации компонентов реакции в мол.% и температуры, при которых проводились измерения. Данные для расчёта должны сохраняться в файлах в определённом формате:</p>
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
        <td rowspan="2">эта таблица получается копированием данных результатов расчётов из программы Хроматэк Аналитик. Помимо этих данных в таблице также могут присутствовать столбцы других значений (напр. высота пика, площадь и т.п.), что не влияет на конечный результат</td>
      </tr>
      <tr>
        <td><i>compound-concentraion</i></td>
        <td>концентрация компонента в мол.%</td>
      </tr>
      <tr>
        <td><i>flow-temperature</i></td>
        <td>температура в точке измерения общего потока газов в °C</td>
        <td rowspan="3">Данные параметры должны быть измерены с помощью газовых часов на выходе из реактора. Эти параметры не являются необходимыми для расчёта характеристик катализатора. Если они не будут указаны в файле, параметры всё равно будут рассчитаны, однако, в результатах будет ошибка, связанная с изменением объёма реагентов.</td>
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
    <p><b>гидрирование CO<sub>2</sub>, расчёт на основе продуктов реакции</b></p>
    <p>Данный метод может быть использован для расчёта конверсии углекислого газа, однако, результат может содержать ошибку, связанную с предположением, что только использованные для расчёта компоненты образовались в результате реакции.</p>
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
  <p>Контроль печи осуществляется с помощью контроллера ОВЕН ТРМ101, связь с которым устанавливается через последовательный порт. Параметры конфигурации контроллера должны быть прописаны в файле <a href="https://github.com/leybodv/pycatalicism/blob/main/pycatalicism/config.py">config.py</a></p>
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
    <p>Осуществляется управление хроматографом Хроматэк Кристалл 5000 через протокол Modbus. Для работы протокола необходимо, чтобы был запущен сервер Modbus, в качестве которого выступают Панель управления и Аналитик, а также специальная программа, которую необходимо установить с установочного диска ПО Хроматэк (см. документацию Modbus из комплекта документации Хроматэк для более детальной инструкции). Перед работой с pycatalytic, необходимо добавить нужные регистры Modbus в Панели управления и Аналитик. Список необходимых регистров прописывается в конфигурации программы и может быть найден здесь: <a href="https://github.com/leybodv/pycatalicism/blob/main/pycatalicism/config.py">config.py</a></p>
    <p><b>Доступные комманды:</b></p>
    <p><code>pycat chromatograph set-method method</code></p>
    <p>Устанавливает инструментальный метод хроматографа. Хроматограф переходит в режим "Подготовка". Список методов должен быть в <a href="https://github.com/leybodv/pycatalicism/blob/main/pycatalicism/config.py">config.py</a>. Если Панель управления и Аналитик не запущены, запускает их, устанавливает соединение с хроматографом. В этом случае программа ждёт успешного запуска Панели управления и Аналитика, а также установления соединения. Если, при этом, хроматограф выключен, программа зависнет.</p>
    <p>Аргументы:</p>
    <p>
      <table>
        <tr>
          <td>method</td>
          <td>инструментальный метод хроматографа</td>
        </tr>
      </table>
    </p>
    <p><code>pycat chromatograph start-analysis</code></p>
    <p>Начинает измерение.</p>
    <p><code>pycat chromatograph set-passport --name NAME [--volume VOL] [--dilution DIL] [--purpose {analysis|graduation}] --operator OP --column COL [--lab-name LN]</code></p>
    <p>Устанавливает значения паспорта хроматограммы. Эта команда должна использоваться только после окончания анализа на хроматографе.</p>
    <p>Необходимые параметры:</p>
    <p>
      <table>
        <tr>
          <td>--name NAME</td>
          <td>название хроматограммы</td>
        </tr>
        <tr>
          <td>--operator OP</td>
          <td>оператор</td>
        </tr>
        <tr>
          <td>--column COL</td>
          <td>название колонки</td>
        </tr>
      </table>
    </p>
    <p>Опциональные параметры:</p>
    <p>
      <table>
        <tr>
          <td>--volume VOL</td>
          <td>объём пробы, 0.5 по умолчанию</td>
        </tr>
        <tr>
          <td>--dilution DIL</td>
          <td>разбавление пробы, 1 по умолчанию</td>
        </tr>
        <tr>
          <td>--purpose {analysis|graduation}</td>
          <td>назначение хроматограммы, analysis по умолчанию</td>
        </tr>
        <tr>
          <td>--lab-name LN</td>
          <td>название лаборатории, Inorganic Nanomaterials по умолчанию</td>
        </tr>
      </table>
    </p>
  <h2 id="mfc">Управление регуляторами расхода газов</h2>
  <p>Программа осуществляет управление регуляторами расхода газов Bronkhorst F201CV для регулирования потока He, CO<sub>2</sub>, O<sub>2</sub>, H<sub>2</sub>, CO или CH<sub>4</sub>. Параметры соответствующих регуляторов расхода газов должны быть прописаны в файле <a href="https://github.com/leybodv/pycatalicism/blob/main/pycatalicism/config.py">config.py</a></p>
  <p><code>pycat mfc set-flow-rate --gas {He|CO2|O2|H2|CO|CH4} --flow-rate FR</code></p>
  <p>Устанавливает поток газа</p>
  <p>
    <table>
      <tr>
        <td>--gas {He|CO2|O2|H2|CO|CH4}</td>
        <td>газ, для которого необходимо установить поток. Программа выбирает регулятор на основе этого значения</td>
      </tr>
      <tr>
        <td>--flow-rate FR</td>
        <td>поток газа в н.мл/мин</td>
      </tr>
    </table>
  </p>
  <p><code>pycat mfc set-calibration --gas {He|CO2|O2|H2|CO|CH4} --calibration-number CN</code></p>
  <p>Устанавливает калибровку регулятора расхода газа</p>
  <p>
    <table>
      <tr>
        <td>--gas {He|CO2|O2|H2|CO|CH4}</td>
        <td>газ, для которого необходимо установить калибровку. Программа выбирает регулятор на основе этого значения</td>
      </tr>
      <tr>
        <td>--calibration-number CN</td>
        <td>номер калибровки, указанный в документации, поставляемой с прибором</td>
      </tr>
    </table>
  </p>
  <p><code>pycat mfc print-flow-rate --gas {He|CO2|O2|H2|CO|CH4}</code></p>
  <p>Выводит измеренный поток газа в консоль в н.мл/мин</p>
  <p>
    <table>
      <tr>
        <td>--gas {He|CO2|O2|H2|CO|CH4}</td>
        <td>газ, для которого нужно показать поток. Программа выбирает регулятор на основе этого значения</td>
      </tr>
    </table>
  </p>
  <h2 id="valves">Управление соленоидными клапанами</h2>
  <p>Программа осуществляет управление соленоидными клапанами VSAA, подключёнными к ардуино согласно схеме <a href="https://github.com/leybodv/pycatalicism/blob/main/wiring/valve-controller_scheme.png">scheme</a>. Соответствие номеров клапанов и соответствующих им газов должно быть прописано в файле <a href="https://github.com/leybodv/pycatalicism/blob/main/pycatalicism/config.py">config.py</a>.</p>
  <p><code>pycat valve set-state --gas G --state {open|close}</code></p>
  <p>Изменяет состояние клапана</p>
  <p>
    <table>
      <tr>
        <td>--gas G</td>
        <td>газ, для которого необходимо изменить состояние клапана. Должен быть прописан в файле конфигурации</td>
      </tr>
      <tr>
        <td>--state {open|close}</td>
        <td>open - открыть клапан<br>close - закрыть клапан</td>
      </tr>
    </table>
  </p>
  <p><code>pycat valve get-state --gas G</code></p>
  <p>Запрашивает состояние клапана</p>
  <p>
    <table>
      <tr>
        <td>--gas G</td>
        <td>газ, для которого запрашивается состояние клапана. Должен быть прописан в файле конфигурации</td>
      </tr>
    </table>
  </p>
  <h2 id="activation">Активация</h2>
  <p>Проведение активации катализатора перед анализом свойств. Для проведения активации все газы должны быть подключены к системе, клапаны открыты. Режим активации задаётся в файле конфигурации, пример которого можно посмотреть здесь: <a href="https://github.com/leybodv/pycatalicism/blob/main/pycatalicism/activation_config.py">activation_config.py</a>. После запуска программа устанавливает заданные в конфигурации потоки, продувает систему в течение 30 мин, греет печь до указанной температуры, проводит выдержку при данной температуре в течение указанного в конфигурации времени и отключают нагрев. После охлаждения ниже определённой температуры потоки газов меняются на новые, указанные в конфигурации. При активации строятся графики зависимости температуры и потоков газов от времени. После окончания активации, для того, чтобы остановить построение графика, нужно нажать Enter в командной строке.</p>
  <p><code>pycat activate --config CONFIG</code></p>
  <p>
    <table>
      <tr>
        <td>--config CONFIG</td>
        <td>путь к файлу конфигурации с параметрами активации</td>
      </tr>
    </table>
  </p>
  <h2 id="measurement">Проведение измерения</h2>
  <p>Проведение измерения состава газа после реактора при различных температурах. Программа проводит продувку хроматографа перед анализом (запускает метод purge на хроматографе), проводит нагрев до температуры измерения, ждёт заданное время, запускает измерение хроматограммы и повторяет данную процедуру для каждой температуры анализа. После окончания анализа программа выключает печь и запускает охлаждение хроматографа. Все параметры измерения должны быть указаны в файле конфигурации, пример которого можно найти здесь: <a href="https://github.com/leybodv/pycatalicism/blob/main/pycatalicism/measurement_config.py">measurement_config.py</a>. При измерении строятся графики зависимости температуры, потоков газов от времени, а также отмечаются моменты времени начала анализа хроматографом.</p>
  <p><code>pycat measure --config CONFIG</code></p>
  <p>
    <table>
      <tr>
        <td>--config CONFIG</td>
        <td>путь к файлу конфигурации с параметрами измерения</td>
      </tr>
    </table>
  </p>
  <h2 id="init-conc-measurement">Проведение измерения исходной концентрации реагентов</h2>
  <p>Проведение серии измерений состава газа при комнатной температуре. Результаты измерений необходимы для расчёта конверсии реакции. Программа устанавливает потоки газов, запускает продувку хроматографа (метод purge) и снимает несколько хроматограмм. По завершении запускает охлаждение хроматографа (метод cooling). Параметры проведения эксперимента должны быть указаны в файле конфигурации, пример которого можно найти здесь: <a href="https://github.com/leybodv/pycatalicism/blob/main/pycatalicism/init_conc_config.py">init_conc_config.py</a>. При измерении строятся графики зависимости температуры, потоков газов от времени, а также отмечаются моменты времени начала анализа хроматографом.</p>
  <p><code>pycat measure-init-concentration --config CONFIG</code></p>
  <p>
    <table>
      <tr>
        <td>--config CONFIG</td>
        <td>путь к файлу конфигурации с параметрами измерения</td>
      </tr>
    </table>
  </p>
  <h2>ТуДу</h2>
    <ul>
      <li>автоматизировать открытие/закрытие соленоидных клапанов</li>
      <li>автоматизировать переключение 3х портового крана</li>
      <li>переписать модуль calc: селективность должна рассчитываться автоматически, если это имеет смысл; должно быть 2 команды <code>calculate activity</code> и <code>calculate conversion</code></li>
      <li>автоматически конвертировать данные с газовых часов в СИ при рассчёте</li>
    </ul>
