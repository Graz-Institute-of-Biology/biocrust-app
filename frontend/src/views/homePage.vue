<template>
    App-Home {{ data_set }}
</template>

<script setup>

import { computed } from 'vue';
import store from '../store';

const data_set = computed(() => store.state.data_set)
</script>