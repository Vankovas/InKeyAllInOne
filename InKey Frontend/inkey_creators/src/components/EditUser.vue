<template>
  <div id="EditUser">
    <div class="modal">
      <div class="modal-header">
        <h1 class="modal-header__title">Edit profile</h1>
      </div>

      <form class="modal-content" @submit.prevent="submitChanges">
        <div class="user-image">
          <img
            class="user-image__img"
            v-bind:style="{
              backgroundImage:
                'url(' + (updatedUser.cover_image_local_url || updatedUser.profile_picture || require('../assets/images/hero-image.jpg')) + ')',
            }"
          />
          <div class="user-image__edit-img">
            <label for="cover-image-upload">Change</label>
            <input id="cover-image-upload" value="Change" type="file" @change="getUserSelectedImage" />
          </div>
        </div>

        <div class="user-info">
          <div class="user-info__panel-group">
            <div class="user-info__panel user-info__panel__firstname">
              <label>First Name</label>
              <input
                :class="{ 'input-error': $v.updatedUser.firstname.$error }"
                name="firstname"
                v-model.trim="updatedUser.firstname"
                @input="setFirstname($event.target.value)"
              />
              <template v-if="errors">
                <div class="error" v-if="!$v.updatedUser.firstname.minLength">
                  First name must have at least {{ $v.updatedUser.firstname.$params.minLength.min }} letters.
                </div>
                <div class="error" v-if="!$v.updatedUser.firstname.maxLength">
                  First name must have at most {{ $v.updatedUser.firstname.$params.maxLength.max }} letters.
                </div>
                <div class="error" v-if="!$v.updatedUser.firstname.alpha">First name must contain only English letters.</div>
              </template>
            </div>

            <div class="user-info__panel user-info__panel__lastname">
              <label>Last Name</label>
              <input
                :class="{ 'input-error': $v.updatedUser.lastname.$error }"
                name="lastname"
                v-model.trim="updatedUser.lastname"
                @input="setLastname($event.target.value)"
              />
              <template v-if="errors">
                <div class="error" v-if="!$v.updatedUser.lastname.minLength">
                  Last name must have at least {{ $v.updatedUser.lastname.$params.minLength.min }} letters.
                </div>
                <div class="error" v-if="!$v.updatedUser.lastname.maxLength">
                  Last name must have at most {{ $v.updatedUser.lastname.$params.maxLength.max }} letters.
                </div>
                <div class="error" v-if="!$v.updatedUser.lastname.alpha">Last name must contain only English letters.</div>
              </template>
            </div>
          </div>

          <div class="user-info__panel-group">
            <div class="user-info__panel user-info__panel__password">
              <label>Password</label>
              <input
                :class="{ 'input-error': updatedUser.password && $v.updatedUser.password.$error }"
                name="password"
                type="password"
                v-model.trim="updatedUser.password"
                @input="setPassword($event.target.value)"
              />
              <template v-if="errors">
                <div class="error" v-if="updatedUser.password && !$v.updatedUser.password.goodPassword">
                  Must contain a lowercase character, uppercase character and a number.
                </div>
                <div class="error" v-if="!$v.updatedUser.password.minLength">
                  Password must have at least {{ $v.updatedUser.password.$params.minLength.min }} letters.
                </div>
                <div class="error" v-if="!$v.updatedUser.password.maxLength">
                  Password must have at most {{ $v.updatedUser.password.$params.maxLength.max }} letters.
                </div>
              </template>
            </div>

            <div class="user-info__panel user-info__panel__confirm-password">
              <label>Confirm Password</label>
              <input
                name="confirmpassword"
                :class="{ 'input-error': $v.updatedUser.confirmPassword.$error }"
                type="password"
                v-model.trim="updatedUser.confirmPassword"
                @input="setConfirmPassword($event.target.value)"
              />
              <template v-if="errors">
                <div class="error" v-if="!$v.updatedUser.confirmPassword.required">Please confirm your password by filling this field as well.</div>
                <div class="error" v-if="updatedUser.confirmPassword && !$v.updatedUser.confirmPassword.sameAsPassword">Passwords do not match.</div>
              </template>
            </div>
          </div>

          <div class="user-info__panel">
            <label>Username</label>
            <input
              name="username"
              :class="{ 'input-error': $v.updatedUser.username.$error }"
              v-model.trim="updatedUser.username"
              @input="setUsername($event.target.value)"
            />
            <template v-if="errors">
              <div class="error" v-if="!$v.updatedUser.username.minLength">
                Username must have at least {{ $v.updatedUser.username.$params.minLength.min }} letters.
              </div>
              <div class="error" v-if="!$v.updatedUser.username.maxLength">
                Username must have at most {{ $v.updatedUser.username.$params.maxLength.max }} letters.
              </div>
            </template>
          </div>

          <div class="user-info__panel">
            <label>Email</label>
            <input
              name="email"
              :class="{ 'input-error': $v.updatedUser.email.$error }"
              v-model.trim="updatedUser.email"
              @input="setEmail($event.target.value)"
            />
            <template v-if="errors">
              <div class="error" v-if="!$v.updatedUser.email.email">Please enter a valid email address.</div>
            </template>
          </div>

          <div class="user-info__panel user-info__panel__description">
            <label>Bio/Description</label>
            <input
              placeholder="Let your fans know what you have going on in your life."
              v-model.trim="updatedUser.description"
              @input="setDescription($event.target.value)"
            />
          </div>

          <div class="user-info__controls">
            <input class="user-info__controls__save btn-secondary" type="submit" value="Save changes" />
            <button type="button" class="user-info__controls__cancel btn-secondary" @click="this.emitHideModal">Cancel</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { email, minLength, maxLength, alpha, sameAs, requiredIf } from 'vuelidate/lib/validators';
import { UPDATE_CREATOR } from '../store/actions.type';

export default {
  name: 'EditUser',
  data() {
    return {
      //The [String + ''] is done so that we make sure we do not mess with the original object.
      updatedUser: {
        username: this.user.username + '',
        firstname: this.user.firstname + '',
        lastname: this.user.lastname + '',
        email: this.user.email + '',
        password: '',
        confirmPassword: '',
        description: this.user.description + '',
        profile_picture: this.user.profile_picture ? this.user.profile_picture + '' : '',
        cover_image_local_url: '',
      },
      //For preventing errors from popping up before submitting
      uiState: 'submit not clicked',
      errors: false,
      empty: true,
    };
  },
  props: {
    hideModal: Function,
    user: Object,
  },
  validations: {
    updatedUser: {
      username: { minLength: minLength(4), maxLength: maxLength(20) },
      firstname: { minLength: minLength(4), maxLength: maxLength(20), alpha },
      lastname: { minLength: minLength(4), maxLength: maxLength(20), alpha },
      email: { email },
      password: {
        minLength: minLength(8),
        maxLength: maxLength(20),
        goodPassword: (password) => {
          return password.length >= 8 && /[a-z]/.test(password) && /[A-Z]/.test(password) && /[0-9]/.test(password);
        },
      },
      confirmPassword: {
        required: requiredIf(function() {
          return this.updatedUser.password ? true : false;
        }),

        sameAsPassword: sameAs(function() {
          console.log(this.updatedUser.password === this.updatedUser.confirmPassword);
          return this.updatedUser.password;
        }),
      },
      description: {},
      cover_image_local_url: {},
      profile_picture: {},
    },
  },
  methods: {
    emitHideModal() {
      this.$emit('hideModal');
    },
    getUserSelectedImage(e) {
      //TODO: Check type of image?
      this.updatedUser.profile_picture = e.target.files[0];
      this.updatedUser.cover_image_local_url = URL.createObjectURL(e.target.files[0]);
      this.$v.updatedUser.profile_picture.$touch();
    },
    setUsername(value) {
      this.updatedUser.username = value;
      this.$v.updatedUser.username.$touch();
    },
    setFirstname(value) {
      this.updatedUser.firstname = value;
      this.$v.updatedUser.firstname.$touch();
    },
    setLastname(value) {
      this.updatedUser.lastname = value;
      this.$v.updatedUser.lastname.$touch();
    },
    setEmail(value) {
      this.updatedUser.email = value;
      this.$v.updatedUser.email.$touch();
    },
    setPassword(value) {
      this.updatedUser.password = value;
      this.$v.updatedUser.password.$touch();
    },
    setConfirmPassword(value) {
      this.updatedUser.confirmPassword = value;
      this.$v.updatedUser.confirmPassword.$touch();
    },
    setDescription(value) {
      this.updatedUser.description = value;
      this.$v.updatedUser.description.$touch();
    },
    submitChanges() {
      this.formTouched = !this.$v.updatedUser.$anyDirty;
      this.errors = this.$v.updatedUser.$anyError;
      this.uiState = 'submit clicked';
      if (this.errors === false && this.formTouched === false) {
        const userData = {};

        ['id', 'username', 'firstname', 'lastname', 'email', 'password', 'confirmPassword', 'description', 'profile_picture'].forEach((key) => {
          console.log(key, this.updatedUser[key], this.$props.user[key]);
          if (key === 'id') return (userData[key] = this.$props.user[key]);
          if (key === 'profile_picture' && this.updatedUser[key] === null) return;
          if (this.updatedUser[key] !== this.$props.user[key] && this.updatedUser[key] !== '') userData[key] = this.updatedUser[key];
        });

        console.log(userData);
        this.$store.dispatch(UPDATE_CREATOR, userData);

        this.emitHideModal();
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../scss/_variables.scss';
@import '../scss/_utilities.scss';
@import '../scss/_mixins.scss';

#EditUser {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(128, 128, 128, 0.5);
  z-index: 1000;

  .modal {
    min-width: 70%;
    max-width: 100%;

    @include respond(laptop) {
      width: 80%;
    }

    @include respond(tablet-land) {
      width: 90%;
    }

    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);

    background-color: white;
    border-radius: 0.5rem;
    overflow: hidden;

    &-header {
      background-color: $color-tertiary;
      color: $color-white;
      padding: 3rem;

      &__title {
        font-size: 2.5rem;
      }
    }

    &-content {
      display: flex;
      justify-content: space-around;
      align-items: center;

      @include respond(tablet-port) {
        display: block;
      }

      width: 100%;
      margin: 0 auto;
      padding: 2rem 0;

      .user-info {
        width: 40%;
        font-size: 2rem;

        @include respond(tablet-port) {
          width: 80%;
          margin: 0 auto;
        }

        &__panel {
          display: inline-block;
          width: 100%;
          margin-bottom: 2rem;

          &-group {
            display: flex;
            justify-content: space-between;
          }

          &__firstname,
          &__lastname,
          &__password,
          &__confirm-password {
            width: 47.5%;
          }

          label {
            font-size: 1.8rem;
            font-weight: 500;
          }

          input {
            font-size: 1.7rem;
            padding: 1rem 2rem;
            background-color: rgba(238, 238, 238, 0.2);
            border: 1px solid #393e46;
            border-radius: 0.3rem;
            width: 100%;
          }
        }

        &__panel > * {
          width: 100%;
        }

        &__controls {
          width: 100%;
          display: flex;
          justify-content: space-evenly;
          margin: 2rem 0;

          &__cancel,
          &__save {
            width: 30%;
            border-radius: 0.5rem;

            font-size: 2rem;
            line-height: 4rem;
          }

          &__save {
            margin-right: 2rem;
            border-color: $color-tertiary;
            background-color: $color-tertiary;
            color: $color-white;

            &:hover {
              background-color: $color-white;
              color: $color-tertiary;
            }
          }

          &__cancel {
            margin-right: 2rem;
            border-color: $color-tertiary;
            background-color: $color-white;
            color: $color-tertiary;

            &:hover {
              background-color: $color-tertiary;
              color: $color-white;
            }
          }
        }
      }

      .user-image {
        position: relative;

        @include respond(tablet-port) {
          width: 30rem;
          margin: 0 auto;
        }

        &__img {
          width: 40rem;
          height: 40rem;
          background-size: cover;
          background-clip: padding-box;
          background-position: center center;
          border-radius: 50%;

          @include respond(tablet-port) {
            width: 30rem;
            height: 30rem;
          }
        }

        &__edit-img {
          z-index: 1000;
          background-color: $color-tertiary;
        }

        &__edit-img {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          display: none;
          cursor: pointer;
          border-radius: 50%;

          label {
            top: 50%;
            left: 50%;
            position: absolute;
            transform: translate(-50%, -50%);
            font-size: 5rem;
            user-select: none;
            color: #fff;
            cursor: pointer;
          }

          input[type='file'] {
            display: none;
          }
        }
      }

      .user-image:hover .user-image__edit-img {
        display: block;
        background: rgba(44, 0, 70, 0.9);
      }
    }
  }

  .input-error {
    border-color: salmon;
  }

  .error {
    width: 100% !important;
    color: salmon;
    font-size: 1.5rem;
  }
}
</style>
