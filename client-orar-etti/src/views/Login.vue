<template>
  <div>
    Login
    <b-form-group
      id="input-group-1"
      label="Email address:"
      label-for="input-1"
      description="We'll never share your email with anyone else."
    >
      <b-form-input
        id="input-1"
        v-model="login_info.email"
        type="email"
        required
        placeholder="Enter email"
      ></b-form-input>
    </b-form-group>

    
  </div>
</template>

<script>
export default {
  data() {
    return {
      login_info: {
        email: "",
        name: "",
        surname: "",
        password: ""
      }
    };
  }
};
</script>

<style>
</style>