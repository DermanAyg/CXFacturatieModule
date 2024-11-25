import { mount } from '@vue/test-utils'
import login from '../../../src/views/login/login.vue'
import { describe, expect, test } from 'vitest'

describe('login.vue', () => {
  test('renders tab login', () => {
    const wrapper = mount(login)
    expect(wrapper.text()).toMatch('login')

  })
})
