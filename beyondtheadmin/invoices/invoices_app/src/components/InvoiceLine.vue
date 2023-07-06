<template>
  <div class="row mb-2">
    <div class="col-md-4">
      <label :for="'description-' + uuid" class="form-label">
        {{$t("Description")}}<span class="asteriskField">*</span>
      </label>
      <textarea class="form-control" rows="2"
                :id="'description-' + uuid"
                v-model="localDescription" required ref="firstLineField"
                :class="{'is-invalid': v$.localDescription.$error}"
                @input="updateLine"
      ></textarea>
      <span class="invalid-feedback" v-if="v$.localDescription.$error">{{ $t("This field is required") }}</span>
    </div>
    <div class="col-md">
      <label :for="'quantity-' + uuid" class="form-label">
        {{$t("Quantity")}}<span class="asteriskField">*</span>
      </label>
      <input type="number" class="form-control"
             :id="'quantity-' + uuid" v-model.number="localQuantity"
             :class="{'is-invalid': v$.localQuantity.$error}"
             @change="updateLine"
      />
       <span class="invalid-feedback" v-if="v$.localQuantity.required.$invalid">
         {{ $t("This field is required") }}
       </span>
       <span class="invalid-feedback" v-if="v$.localQuantity.minValue.$invalid">
         {{ $t("Should be > 0") }}
       </span>
    </div>
    <div class="col-md">
      <label :for="'unit-' + uuid" class="form-label">
        {{$t("Unit")}}<span class="asteriskField">*</span>
      </label>
      <select class="form-control"
              v-model="localUnit" :id="'unit-' + uuid"
              :class="{'is-invalid': v$.localUnit.$error}"
              @change="updateLine"
      >
        <option value="h">{{ $t('Hour') }}</option>
        <option value="nb">{{$t("Number")}}</option>
      </select>
      <span class="invalid-feedback" v-if="v$.localUnit.required.$invalid">
        {{ $t("This field is required") }}
      </span>
    </div>
    <div class="col-md">
      <label :for="'price-' + uuid" class="form-label">
        {{$t("Unit price")}}<span class="asteriskField">*</span>
      </label>
      <input type="number" class="form-control" step="0.01"
             v-model.number="localPrice" :id="'price-' + uuid"
              :class="{'is-invalid': v$.localPrice.$error}"
             @input="updateLine"
      />
      <span class="invalid-feedback" v-if="v$.localPrice.required.$invalid">
        {{ $t("This field is required") }}
      </span>
    </div>
    <div class="col-md">
      <label class="form-label" :for="'total-' + uuid">
        {{ $t("Total" )}}
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
import { useVuelidate } from '@vuelidate/core'
import {required, minValue} from '@vuelidate/validators'

export default {
  props: {
    line: {
      type: Object,
      required: false,
    }
  },
  data() {
    return {
      localDescription: this.line?.description || '',
      localQuantity: this.line?.quantity || 0,
      localUnit: this.line?.unit || 'h',
      localPrice: this.line?.price_per_unit || 0,
    };
  },
  computed: {
    total() {
      return Math.round(this.localQuantity * this.localPrice * 100) / 100;
    },
  },
  methods: {
    async removeLine() {
      this.$emit('remove');
    },
    focus() {
      this.$refs.firstLineField.focus();
    },
    updateLine() {
     this.$emit('update-line', {
        description: this.localDescription,
        quantity: this.localQuantity,
        unit: this.localUnit,
        price_per_unit: this.localPrice,
        uid: this.line.uid,
        total: this.total,
      }
     );
    },
  },
  validations: {
    localDescription: { required },
    localQuantity: { required, minValue: minValue(0.1) },
    localUnit: { required },
    localPrice: { required },
  },
  setup(){
    const { t } = useI18n();
    return {
      t,
      v$: useVuelidate(),
    }
  }
};

</script>
