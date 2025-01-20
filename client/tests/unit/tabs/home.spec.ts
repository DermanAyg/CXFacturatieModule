import { mount } from '@vue/test-utils'
import home from '../../../src/views/tabs/home.vue'
import { describe, expect, test } from 'vitest'

describe('home.vue', () => {
  test('renders tab home', () => {
    const wrapper = mount(home)
    expect(wrapper.text()).toMatch('home')

  })
})
