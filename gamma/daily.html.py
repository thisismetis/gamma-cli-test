<table>
    <tr>
        {% for day in ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] %}
            <th> {{ day }}</th>
        {% endfor %}
    </tr>


    {% for week in range(1,pair_df.week.max()+1) %}
      {% set weekloop = loop %}
      <tr>
      {% for day in range(0,6) %}
          {% if loop.first %}
            <th>{{ "Week {}".format(week) }}</th>
          {% else %}

            {% set pair = pair_df.query("(day == {}) and (week == {})".format(day,week)) %}

            {% set lessons = lesson_df.query("(day == {}) and (week == {})".format(day,week)).sort_values("order") %}

            <td>
            {%  if (pair.shape[0] > 0)  or (lessons.shape[0] > 0) %}


                  Instruction Time: {{ lessons.duration.sum() }}m <br>
                  {% if pair.shape[0] > 0 %}
                    {% set pair = pair.to_dict("records")[0] %}
                    <a href="{{ '/pairs/' + pair['pair'] }}" >• Pair: {{ pair['title'] }}</a> ({{ pair['duration'] }}m)<br>
                  {% endif %}
                  {% for lesson in lessons.to_dict("records") %}
                  <a href="{{ '/curriculum/' + lesson['project'] + '/' + lesson['lesson'] }}" >• {{ lesson["title"] }}</a> ({{ lesson['duration'] }}m)<br>
                  {% endfor %}



            {% endif %}
            </td>

        {% endif %}

    {% endfor %}
    </tr>
    {% endfor %}
</table>