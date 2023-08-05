<div>
<el-card shadow="hover" class="box-card">
  <el-main>

    <el-row :gutter="10">
      {% for field in table %}
      {% if not loop.first %}


      <el-col :xs="24" :sm="12" :md="8" :lg="6" :xl="6" class="filter-item">
        {% if field.field_type in ['date','datetime'] %}
        <el-date-picker
            v-model="queryParams.{{ field.field_name }}"
            type={{field.field_type}}
            placeholder="选择{{ field.label }}"
        >
        </el-date-picker>
        {% elif field.field_type == 'choice' %}
        <el-select v-model="queryParams.{{ field.field_name }}" placeholder="请选择{{ field.label }}">
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
            v-model="queryParams.{{ field.field_name }}"
            clearable
        ></el-input>
        {% endif %}
      </el-col>
      {% endif %}{% endfor %}
      <el-button
          title="查询"
          @click="query"
          type="primary"
      >查询
      </el-button>
    </el-row>
  </el-main>
</el-card>
</div>