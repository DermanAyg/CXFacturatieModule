import { mount } from '@vue/test-utils'
import registreer from '../../../src/views/registreer/registreer.vue'
import { describe, expect, test } from 'vitest'

describe('registreer.vue', () => {
  test('renders tab registreer', () => {
    const wrapper = mount(registreer)
    expect(wrapper.text()).toMatch('registreer')

  })
})
