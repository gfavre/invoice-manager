<template>
  <div class="row mb-2">
    <div class="col-md-4">
      <label :for="'description-' + uuid" class="form-label">
        Description *
      </label>
      <textarea class="form-control" rows="2"
                :id="'description-' + uuid"
                v-model="localDescription" required ref="firstLineField"
                @blur="updateLine"
      ></textarea>
    </div>
    <div class="col-md">
      <label :for="'quantity-' + uuid" class="form-label">
        Quantité *
      </label>
      <input type="number" class="form-control"
             :id="'quantity-' + uuid" v-model.number="localQuantity" required
             @change="updateLine"
      />
    </div>
    <div class="col-md">
      <label :for="'unit-' + uuid" class="form-label">
        Unité *
      </label>
      <select class="form-control"
              v-model="localUnit" :id="'unit-' + uuid" required
              @change="updateLine"
>
        <option value="h">Hour</option>
        <option value="nb">Number</option>
      </select>
    </div>
    <div class="col-md">
      <label :for="'price-' + uuid" class="form-label">
        Prix unitaire *
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
        Total
      </label>
      <span class="form-text total" :id="'total-' + uuid">{{ $formatAmount(total) }}</span>
    </div>
    <div class="col-md">
      <label>&nbsp;</label><br>
      <a href="#" class="btn btn-link remove-line " @click.prevent="removeLine()">Supprimer</a>
    </div>
  </div>
</template>

<script>
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
      // Get all required input fields in the component
      const requiredInputs = this.$el.querySelectorAll('.form-control[required]');

      // Loop through each required input field
      requiredInputs.forEach((input) => {
        // Check if the input is empty
        if (!input.value) {
          // Add the is-invalid class to the input
          input.classList.add('is-invalid');

          // Create a new error message element
          const errorMessage = document.createElement('div');
          errorMessage.classList.add('invalid-feedback');
          errorMessage.innerHTML = 'This field is required.';

          // Insert the error message after the input
          input.parentNode.insertBefore(errorMessage, input.nextSibling);
        } else {
          // Remove the is-invalid class and error message if they exist
          input.classList.remove('is-invalid');
          const errorMessage = input.nextElementSibling;
          if (errorMessage && errorMessage.classList.contains('invalid-feedback')) {
            errorMessage.parentNode.removeChild(errorMessage);
          }
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

};

</script>
