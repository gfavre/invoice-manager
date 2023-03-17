<template>
  <div class="invoice-line">
    <input type="text" v-model="description">
    <input type="number" v-model="quantity">
    <input type="number" v-model="price">
    <button @click="updateLine">Update</button>
  </div>

  <!--
     <div id="item-" data-item-id="" data-item-url="" class="row invoice-line">
      <div class="col-4">
        <label for="description-" class="form-label">
          Description
        </label>
        <textarea class="form-control description" id="description-" rows="3"></textarea>
      </div>
      <div class="col">
        <label for="quantity-" class="form-label">
          Quantité
        </label>
        <input type="number" step="any" value="" class="form-control quantity" id="quantity-">
      </div>
      <div class="col">
        <label for="unit-" class="form-label">
          Unité
        </label>
        <select class="unit form-control" id="unit-">
          <option value="h">Heure</option>
          <option value="nb">Nombre</option>
        </select>
      </div>
      <div class="col">
        <label for="price_per_unit-" class="form-label">
          Prix unitaire
        </label>
        <input type="number" step=".01" value="0" class="form-control price_per_unit" id="price_per_unit-">
      </div>
      <div class="col">
        <label for="total-" class="form-label">
          Total
        </label>
        <span class="form-text total" id="total-"></span>
      </div>
      <span class="item-action">
        <label>&nbsp;</label><br>
        <a href="" class="remove-line form-text" data-api-url="">Supprimer</a>
      </span>
    </div>
    -->


</template>

<script>
export default {
  name: "InvoiceLine",
  props: {
    lineId: {
      type: Number,
      required: true
    },
    initialDescription: {
      type: String,
      required: true
    },
    initialQuantity: {
      type: Number,
      required: true
    },
    initialPrice: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      description: this.initialDescription,
      quantity: this.initialQuantity,
      price: this.initialPrice
    };
  },
  methods: {
    updateLine() {
      // call the REST API to update the line
      // you can use Axios or another library to make the API call
      // the line ID and updated data can be passed as parameters
      // once the API call is complete, you can update the component's data as needed
      // you can also emit an event to notify the parent component that the line has been updated
    }
  }
};
</script>
