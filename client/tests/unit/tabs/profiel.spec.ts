import { mount } from '@vue/test-utils'
import profiel from '../../../src/views/tabs/profiel.vue'
import { describe, expect, test } from 'vitest'

describe('profiel.vue', () => {
  test('renders tab profiel', () => {
    const wrapper = mount(profiel)
    expect(wrapper.text()).toMatch('profiel')

  })
})
