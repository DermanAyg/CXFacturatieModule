import { mount } from '@vue/test-utils'
import facturen from '../../../src/views/tabs/facturen.vue'
import { describe, expect, test } from 'vitest'

describe('facturen.vue', () => {
  test('renders tab facturen', () => {
    const wrapper = mount(facturen)
    expect(wrapper.text()).toMatch('facturen')

  })
})
