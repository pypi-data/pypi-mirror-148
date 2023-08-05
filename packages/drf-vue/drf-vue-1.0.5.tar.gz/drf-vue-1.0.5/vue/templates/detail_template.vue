<el-main>
 {%- macro treedot(dict,string) -%}
      {%- for key, field in dict.items() -%}
          {%- if field is mapping  and not "field_type" in field  -%}
              {%- if string -%}
                  {%- set str = string ~ '.' ~ key  -%}
              {%- else -%}
                  {%- set str = key  -%}
              {%- endif -%}
              <el-tab-pane label="{{ str ~ '.' ~ key }}" name="{{ str ~ '.' ~ key}}">{{ str ~ '.' ~ key }}</el-tab-pane>

              {{ treedot(field,str) }}

          {%- else -%}
        {%- if string %}
                      {% if field.field_type in ['date','datetime'] %}
                      <el-date-picker
                          v-model="queryParams.{{ string ~ '.' ~ key }}"
                          type={{field.field_type}}
                          placeholder="选择{{ field.label }}"
                      >
                      </el-date-picker>
                      {% elif field.field_type == 'choice' %}
                      <el-select v-model="queryParams.{{ string ~ '.' ~ key }}" placeholder="请选择{{ field.label }}">
                        <el-option
                            v-for="item in {{ field.choice_text }}_options"
                            :key="item.value"
                            :label="item.text"
                            :value="item.value">
                        </el-option>
                      </el-select>
                      {% else %}
                      <el-input
                          placeholder="请输入{{ field.label }}"
                          v-model="queryParams.{{ string ~ '.' ~ key }}"
                          clearable
                      ></el-input>
                      {% endif %}



              {%- else %}

                  {% if field.field_type in ['date','datetime'] %}
                      <el-date-picker
                          v-model="queryParams.{{key}}.{{ field.field_name }}"
                          type={{field.field_type}}
                          placeholder="选择{{ field.label }}"
                      >
                      </el-date-picker>
                      {% elif field.field_type == 'choice' %}
                      <el-select v-model="queryParams.{{key}}.{{ field.field_name }}" placeholder="请选择{{ field.label }}">
                        <el-option
                            v-for="item in {{ field.choice_text }}_options"
                            :key="item.value"
                            :label="item.text"
                            :value="item.value">
                        </el-option>
                      </el-select>
                      {% else %}
                      <el-input
                          placeholder="请输入{{ field.label }}"
                          v-model="queryParams.{{key}}.{{ field.field_name }}"
                          clearable
                      ></el-input>
                      {% endif %}

              {%- endif -%}
          {%- endif -%}
      {%- endfor -%}
  {%- endmacro -%}
  {{ treedot(table,none) }}
</el-main>



