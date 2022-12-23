<h1>Протокол связи между pycat и pycatuino</h1>
<h2>v.0</h2>
<p>Обмен сообщениями происходит в ASCII формате. Ведущее устройство отправляет сообщение в формате "ведущий -> ведомый". На каждое сообщение ведомое устройство отправляет ответ в формате "ведомый -> ведущий".</p>
<p>Формат сообщения (ведущий -> ведомый):</p>
<table>
  <tr>
    <td>@</td>
    <td>&lt;command&gt;</td>
    <td>.</td>
    <td>&lt;devnum&gt;</td>
    <td>.</td>
    <td>&lt;value&gt;</td>
    <td>#</td>
  </tr>
</table>
<table>
  <tr>
    <td>&lt;command&gt;</td>
    <td>SET - установить значение клапана &lt;devnum&gt;<br>GET - запросить состояние клапана &lt;devnum&gt; (значение &lt;value&gt; должно быть NONE)<br>HSH - приветствие (значение devnum может быть любым от 1 до 5)</td>
  </tr>
  <tr>
    <td>&lt;devnum&gt;</td>
    <td>Номер клапана от 1 до 5</td>
  </tr>
  <tr>
    <td>&lt;value&gt;</td>
    <td>OPEN - открыть клапан<br>CLOSE - закрыть клапан<br>NONE - значение при запросе состояния клапана<br>NISMF - слово приветствие</td>
  </tr>
</table>
<p>Формат ответа (ведомый -> ведущий)</p>
<table>
  <tr>
    <td>@</td>
    <td>&lt;devstat&gt;</td>
    <td>.</td>
    <td>&lt;value&gt;</td>
    <td>#</td>
  </tr>
</table>
<table>
  <tr>
      <td>&lt;devstat&gt;</td>
      <td>OK - последняя операция выполнена успешно<br>ERR - последняя операция выполнена с ошибками<br>HSH - ответ на приветствие<br>ANS - ответ на команду GET</td>
  </tr>
  <tr>
    <td>&lt;value&gt;</td>
    <td>OPEN|CLOSE - открыт или закрыт клапан (высылается при успешном выполнении последней операции или при ответе на запрос ведущего устройства)<br>&lt;errcode&gt; - код ошибки<br>DBQWT - слово ответа на приветствие</td>
  </tr>
</table>
<p>Коды ошибок</p>
<table>
  <tr>
    <td>MSGFMT</td>
    <td>Неверный формат сообщения</td>
  </tr>
  <tr>
    <td>DVNM</td>
    <td>Ошибка в номере клапана &lt;devnum&gt;</td>
  </tr>
  <tr>
    <td>HNDSHK</td>
    <td>Ошибка в слове приветствия</td>
  </tr>
  <tr>
    <td>VL</td>
    <td>Ошибка в значении &lt;value&gt;</td>
  </tr>
</table>
