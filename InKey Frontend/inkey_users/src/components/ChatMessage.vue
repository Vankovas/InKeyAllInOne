<template>
  <div id="ChatMessage">
    <div class="info">
      {{ `[${data.timestamp}]` }} <span :style="{ color: data.user.color }">{{ `${data.user.username}:` }}</span>
    </div>
    <div class="message">{{ data.message }}</div>
  </div>
</template>

<script>
//if rerouting to user profile, check if the id parses into a number succ.
export default {
  name: 'ChatMessage',
  props: {
    data: Object,
  },
};
</script>
<style lang="scss" scoped>
#ChatMessage {
  display: flex;

  & > * {
    padding-left: 1rem;
    font-size: 2rem;
  }

  .info {
    white-space: nowrap;
    font-weight: bold;
  }

  .message {
    width: 100%;
  }
}
</style>
