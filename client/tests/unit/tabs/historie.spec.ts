import { mount } from '@vue/test-utils'
import historie from '../../../src/views/tabs/historie.vue'
import { describe, expect, test } from 'vitest'

describe('historie.vue', () => {
  test('renders tab historie', () => {
    const wrapper = mount(historie)
    expect(wrapper.text()).toMatch('historie')

  })
})
