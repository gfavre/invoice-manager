<template>
  <div class="row mb-2">
    <div class="col-md-4">
      <label :for="'description-' + uuid" class="form-label">
        {{$t("Description")}}<span class="asteriskField">*</span>
      </label>
      <textarea class="form-control" rows="2"
                :id="'description-' + uuid"
                v-model="localDescription" required ref="firstLineField"
                @blur="updateLine"
      ></textarea>
    </div>
    <div class="col-md">
      <label :for="'quantity-' + uuid" class="form-label">
        {{$t("Quantity")}}<span class="asteriskField">*</span>
      </label>
      <input type="number" class="form-control"
             :id="'quantity-' + uuid" v-model.number="localQuantity" required
             @change="updateLine"
      />
    </div>
    <div class="col-md">
      <label :for="'unit-' + uuid" class="form-label">
        {{$t("Unit")}}<span class="asteriskField">*</span>
      </label>
      <select class="form-control"
              v-model="localUnit" :id="'unit-' + uuid" required
              @change="updateLine"
      >
        <option value="h">{{ $t('Hour') }}</option>
        <option value="nb">{{$t("Number")}}</option>
      </select>
    </div>
    <div class="col-md">
      <label :for="'price-' + uuid" class="form-label">
        {{$t("Unit price")}}<span class="asteriskField">*</span>
      </label>
      <div class="input-group">
        <input type="number" class="form-control" step="0.01"
               v-model.number="localPrice" :id="'price-' + uuid" required
               @input="updateLine"
        />
      </div>
    </div>
    <div class="col-md">
      <label class="form-label" :for="'total-' + uuid">
        {{$t("Total")}}
      </label>
      <span class="form-text total" :id="'total-' + uuid">{{ $formatAmount(total) }}</span>
    </div>
    <div class="col-md">
      <label>&nbsp;</label><br>
      <a href="#" class="btn btn-link remove-line " @click.prevent="removeLine()">{{ $t("Remove") }}</a>
    </div>
  </div>
</template>

<script>
import { useI18n } from 'vue-i18n';

export default {
  props: {
    description: String,
    quantity: {
      type: Number,
      validator: (value) => {
        return !isNaN(parseFloat(value)) && isFinite(value);
      },
    },
    unit: String,
    price: {
      type: Number,
      validator: (value) => {
        return !isNaN(parseFloat(value)) && isFinite(value);
      },
    },
    lineId: {
      type: Number,
      required: false,
    },
    invoiceId: Number,
    uuid: String,
    apiUrl: String,
  },
  data() {
    return {
      localDescription: this.description || '',
      localQuantity: this.quantity || 0,
      localUnit: this.unit || 'h',
      localPrice: this.price || 0,
    };
  },
  computed: {
    total() {
      return Math.round(this.localQuantity * this.localPrice * 100) / 100;
    },
    lineUrl() {
      return `${this.apiUrl}${this.lineId}/`
    },
    isSaveable() {
      return this.localDescription && this.localQuantity && this.localUnit && this.localPrice;
    }
  },
  methods: {
    async saveLine() {
      const data = {
        description: this.localDescription,
        quantity: this.localQuantity,
        unit: this.localUnit,
        price_per_unit: this.localPrice,
      };
      let response;
      if (!this.lineId) {
        response = await this.$http.post(this.apiUrl, data);
      } else {
        response = await this.$http.put(this.lineUrl, data);
      }
      return response;
    },
    async removeLine() {
      if (this.lineId) {
        await this.$http.delete(this.lineUrl)
      }
      this.$emit('remove');
    },
    focus() {
      this.$refs.firstLineField.focus();
    },
    markRequiredFields() {
      this.$el.querySelectorAll('.is-invalid').forEach((el) => {
        el.classList.remove('is-invalid');
      });
      this.$el.querySelectorAll('.invalid-feedback').forEach((el) => {
        el.remove();
      });

      // Add error messages for missing required fields
      const requiredFields = this.$el.querySelectorAll('.form-control[required]');
      requiredFields.forEach((field) => {
        if (!field.value) {
          field.classList.add('is-invalid');
          const errorEl = document.createElement('div');
          errorEl.classList.add('invalid-feedback');
          errorEl.innerText = this.$t('This field is required');
          field.parentNode.insertBefore(errorEl, field.nextSibling);
        }
      });
    },
    updateLine() {
      if (!this.isSaveable) {
        return
      }
      this.saveLine().then(response => {
        this.$emit('update-line', {
          id: response.data.id,
          description: this.localDescription,
          quantity: this.localQuantity,
          unit: this.localUnit,
          price: this.localPrice,
          total: this.total,
          uuid: this.uuid,
        });
      });
    },
  },
  watch: {
    isSaveable() {
      this.markRequiredFields();
    },
    total() {
      this.markRequiredFields();
    }
  },
  setup(){
    const { t } = useI18n();
    return { t }
  }

};

</script>
