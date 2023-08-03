<template>
  <div class="typeahead-wrap" :class="containerClass" >
    <div class="input-wrap" >
      <input type="text" class="form-control typeahead"
             v-model="searchQuery"
             @input="searchItems" @focus="searchItems"
      />
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search tp-icon search-icon" viewBox="0 0 16 16"><path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"></path></svg>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="currentColor" aria-hidden="true" class="tp-icon clear-icon" :class="$attrs.class" @click="clearSearchQuery"><path d="M23.057 7.057l-16 16c-0.52 0.52-0.52 1.365 0 1.885s1.365 0.52 1.885 0l16-16c0.52-0.52 0.52-1.365 0-1.885s-1.365-0.52-1.885 0z"></path><path d="M7.057 8.943l16 16c0.52 0.52 1.365 0.52 1.885 0s0.52-1.365 0-1.885l-16-16c-0.52-0.52-1.365-0.52-1.885 0s-0.52 1.365 0 1.885z"></path></svg>
    </div>
    <div class="dropdown">
      <ul class="dropdown-menu show" :class="{ 'd-none': !isDropdownOpen }" ref="dropdownMenu">
        <li v-for="(item, index) in highlightedItems" :key="item.id" class="dropdown-item"
            @click="selectItem(item)" :class="{ 'bg-light': index === highlightedIndex }">
          <span v-html="item.highlightedName"></span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    items: {
      type: Array,
      required: true,
    },
    value: {
      type: String,
      default: '',
    },
    isGrouped: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      searchQuery: this.value,
      isDropdownOpen: false,
      highlightedIndex: 0,
    };
  },
  computed: {
    highlightedItems() {
      const regex = new RegExp(`(${this.searchQuery})`, 'gi');
      return this.reactiveItems.map(item => {
        const highlightedName = item.name.replace(regex, '<strong>$1</strong>');
        return { ...item, highlightedName };
      }).filter(item => item.highlightedName !== item.name);
      //return this.items.filter((item) => item.name.toLowerCase().includes(this.searchQuery.toLowerCase()));
    },
    reactiveItems() {
      /* note for self: this.items is a prop, so it's not reactive. We need to return a copy of it to make it
      reactive. By using the spread operator (...), it creates a new array with the same elements as items, which can
      be modified without affecting the original array. */
      return [...this.items];
    },
    containerClass(){
      const additionalClass = this.isGrouped ? 'grouped' : '';
      return `${this.$attrs.class} ${additionalClass}`;
    },
  },
  methods: {
    closeDropdown() {
      this.isDropdownOpen = false;
    },
    clearSearchQuery() {
      this.searchQuery = '';
      this.closeDropdown();
      this.$emit('select', null);
    },
    searchItems() {
      this.isDropdownOpen = true;
    },
    selectItem(item) {
      this.searchQuery = item.name;
      this.closeDropdown();
      this.$emit('select', item);
    },
    onKeydown(event) {
      switch (event.key) {
        case 'ArrowDown':
          this.highlightNext();
          break;
        case 'ArrowUp':
          this.highlightPrevious();
          break;
        case 'Enter':
          this.selectItem(this.highlightedItems[this.highlightedIndex]);
          break;
        case 'Tab':
          this.closeDropdown();
          break;
        case 'Escape':
          this.closeDropdown();
          break;
      }
    },
    highlightPrevious() {
      if (!this.isDropdownOpen) {
        return;
      }
      if (this.highlightedIndex > 0) {
        this.highlightedIndex--;
      }
    },
    highlightNext() {
      if (!this.isDropdownOpen) {
        return;
      }
      if (this.highlightedIndex < this.highlightedItems.length - 1) {
        this.highlightedIndex++;
      }
    },
    onWindowClick(event) {
      if (this.$refs.dropdownMenu) {
        if (this.$refs.dropdownMenu.contains(event.target) || !event.target.classList.contains('typeahead')){
          this.closeDropdown()
        }
      }
    },
  },
  emits: ['select'],
  mounted() {
    window.addEventListener('click', this.onWindowClick);
    window.addEventListener('keydown', this.onKeydown);
  },
  beforeUnmount() {
    window.removeEventListener('click', this.onWindowClick);
    window.removeEventListener('keydown', this.onKeydown);
  },
  watch: {
    value(newValue) {
      this.searchQuery = newValue;
    },
    items(newValue) {
      this.reactiveItems = [...newValue];
    },
  },
};
</script>
<style>
.grouped {
  flex: 1 1 auto;
}
.grouped .form-control{
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}
.bi {
  display: inline-block;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1;
  text-align: center;
  white-space: nowrap;
  vertical-align: middle;
  user-select: none;
}
.dropdown-item {
  cursor: pointer;
}
.input-wrap {
  position: relative;
  width: 100%;
  box-sizing: unset;
}
.typeahead {
  padding-left: 35px;
}
.tp-icon {
  stroke: currentColor;
  fill: currentColor;
  stroke-width: 0;
  display: inline-block;
  box-sizing: content-box;
  font-size: 1.5rem;
  padding: 6px 12px;
  width: 1rem;
  height: 1rem;
  color: #959595;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}
.search-icon {
  left: 0;
}
.clear-icon {
  cursor: pointer;
  right: 0;
}
.typeahead-wrap.is-invalid .form-control {
  border-color: var(--red);
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='none' stroke='%23e74a3b' viewBox='0 0 12 12'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23e74a3b' stroke='none'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right calc(0.375em + 0.1875rem) center;
  background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
  padding-right: calc(1.5em + 0.75rem)!important;
}

.typeahead-wrap.is-invalid .clear-icon {
  right: 1.25rem;
}

</style>
