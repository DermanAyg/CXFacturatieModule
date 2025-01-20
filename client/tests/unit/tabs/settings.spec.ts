import { mount } from '@vue/test-utils'
import settings from '../../../src/views/tabs/settings.vue'
import { describe, expect, test } from 'vitest'

describe('settings.vue', () => {
  test('renders tab settings', () => {
    const wrapper = mount(settings)
    expect(wrapper.text()).toMatch('settings')

  })
})
