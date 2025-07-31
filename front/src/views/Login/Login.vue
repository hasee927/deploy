<script setup lang="ts">
import { LoginForm, TelephoneCodeForm } from './components'
import { ThemeSwitch } from '@/components/ThemeSwitch'
import { LocaleDropdown } from '@/components/LocaleDropdown'
import { useI18n } from '@/hooks/web/useI18n'
import { underlineToHump } from '@/utils'
import { useAppStore } from '@/store/modules/app'
import { useDesign } from '@/hooks/web/useDesign'
import { ref } from 'vue'
import { ElScrollbar } from 'element-plus'
import { computed } from 'vue'
import { ElButton } from 'element-plus'

const { getPrefixCls } = useDesign()

const prefixCls = getPrefixCls('login')

const appStore = useAppStore()

const { t } = useI18n()

const isPasswordLogin = ref(true)
const logo = computed(() => appStore.getLogoImage)

const toTelephoneLogin = () => {
  isPasswordLogin.value = false
}

const toPasswordLogin = () => {
  isPasswordLogin.value = true
}

const icpNumber = computed(() => appStore.getIcpNumber)
const toICO = () => {
  window.open('https://beian.miit.gov.cn/#/Integrated/index')
}
</script>

<template>
  <div
    :class="prefixCls"
    class="h-[100%] relative lt-xl:bg-[var(--login-bg-color)] lt-sm:px-10px lt-xl:px-10px lt-md:px-10px"
  >
    <ElScrollbar class="h-full">
      <div class="relative flex mx-auto min-h-100vh">
        <div
          :class="`${prefixCls}__left flex-1 bg-gray-500 bg-opacity-20 relative p-30px lt-xl:hidden`"
        >
          <div class="flex items-center relative text-white">
            <!-- <img :src="logo" alt="" class="w-48px h-48px mr-10px" /> -->
            <!-- <span class="text-20px font-bold">{{ underlineToHump(appStore.getTitle) }}</span> -->
			<!-- <img style="width: 160px; height: 160px;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKsAAACrAQAAAAAxk1G0AAACwklEQVR4nOWXu63jMBBFR2DAzGqAANtgxpasBvRpQGqJGdsQwAbEjAGh2Utb7/kFG+wo2QXWcOITDDmfezkm/t1np/8bH0RDVKvjLdqlqByok+PMdQg2x3Q4enjqIogcB/MkxDPkzVR4iTTcwlNIudSJqS9qu4tHzysZ0oid+B7m+iQ+cbtoc6jTJ3kBftXbfL4/2/DHGJ9ciPw+RRxi+s9ASHBAyApMpFZPRLWT49On09kDN3UolTpJbTewNqNOqzM9SsVqCXW4gdsdE0JytMwqxyu2CL86vw/RzsRbULPbBzk+CcDOjkZfHw5ZmkmOOSAYrwCuHfJw7xmU4VMrLgnhoUvMzhSuI0U4R9MFXJBnr6AJ1H6R48OlJeKCOznYw95fsWUYAhp9a/io6+jsSXWQY4bbaTR8f740+hoiMUawp6cpGnTscGjg1wxKMIq9kj31PsB3GeWv0x0MZactGELfNEHf3Q0c0XPbRImqe3TM8g3MBlmOGj7RVJ6/KijD7RnZR4gg1ge6x9cFRfjAE1RgnNT8O8Kx3mqQ4Vx41rUrvAJzmj0vcnxihDE+aJ2Hd+KCl0OIcA7qoDRrnJCaMlr/xRiD0xe8HlCVhSaQa3cDo+3NJKhvqsJN7SbHHJoUeiSHE0olpxY5zhi6qOAxLV2Pd5I3OeaCAmNwYN7Icp/CPsjx4VFmzCCmGEZlD//OUoZP2odWJMSuGGf6fkkkGMU+MDitdZC4XSltcnx6ADt7eukSanivLUJMPMNaCuyf8RQcOrEcH7pi5ZmwD2q4hcK7lOX42n1eyh492DWDIowtbEKvUHVMYlFLfM+gDOP1GDWhVxOWuLaz2HwDYwsL7XmHf3Nz8bcub2Ds1/b0tS/8Y0eW4rYjDFjBonm6ywdlmCtk9KSEmpGrRN/JCzB+oVcnwTUJS+Xh0yLHf+F/2j+OfwEp1ywL8E1V4gAAAABJRU5ErkJggg==" alt="" class="w-48px h-48px mr-10px" /> -->
          </div>
          <div class="flex justify-center items-center h-[calc(100%-60px)]">
            <TransitionGroup
              appear
              tag="div"
              enter-active-class="animate__animated animate__bounceInLeft"
            >
              <img src="@/assets/svgs/login-box-bg.svg" key="1" alt="" class="w-350px" />
              <div class="text-3xl text-white" key="2">{{ t('login.welcome') }}</div>
              <div class="mt-5 font-normal text-white text-14px" key="3">
                {{ t('login.message') }}
              </div>
            </TransitionGroup>
          </div>
        </div>
        <div class="flex-1 p-30px lt-sm:p-10px dark:bg-[var(--login-bg-color)] relative">
          <div
            class="flex justify-between items-center text-white at-2xl:justify-end at-xl:justify-end"
          >
            <div class="flex items-center at-2xl:hidden at-xl:hidden">
              <!-- <img :src="logo" alt="" class="w-48px h-48px mr-10px" /> -->
              <span class="text-20px font-bold">{{ underlineToHump(appStore.getTitle) }}</span>
            </div>

            <div class="flex justify-end items-center space-x-10px">
              <ThemeSwitch />
              <LocaleDropdown class="lt-xl:text-white dark:text-white" />
            </div>
          </div>
          <Transition appear enter-active-class="animate__animated animate__bounceInRight">
            <div
              class="h-full flex items-center m-auto w-[100%] at-2xl:max-w-500px at-xl:max-w-500px at-md:max-w-500px at-lg:max-w-500px"
            >
              <LoginForm
                v-if="isPasswordLogin"
                class="p-20px h-auto m-auto lt-xl:rounded-3xl lt-xl:light:bg-white"
                @to-telephone="toTelephoneLogin"
              />
              <TelephoneCodeForm
                v-else
                class="p-20px h-auto m-auto lt-xl:rounded-3xl lt-xl:light:bg-white"
                @to-password="toPasswordLogin"
              />
            </div>
          </Transition>
          <div class="text-14px text-white font-normal absolute bottom-5 right-10">
            <ElButton type="info" link @click="toICO">{{ icpNumber }}</ElButton>
          </div>
        </div>
      </div>
    </ElScrollbar>
  </div>
</template>

<style lang="less" scoped>
@prefix-cls: ~'@{namespace}-login';

.@{prefix-cls} {
  overflow: auto;

  &__left {
    &::before {
      position: absolute;
      top: 0;
      left: 0;
      z-index: -1;
      width: 100%;
      height: 100%;
      background-image: url('@/assets/svgs/login-bg.svg');
      background-position: center;
      background-repeat: no-repeat;
      content: '';
    }
  }
}
</style>
