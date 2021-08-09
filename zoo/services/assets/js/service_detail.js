import '../style/service_detail.less'
import 'fomantic-ui-css/semantic.min.js'
import Mustache from 'mustache'
import Vue from 'vue'
import { VuePlugin } from 'vuera'
import SwaggerUI from 'swagger-ui-react'
import 'swagger-ui-react/swagger-ui.css'


Vue.use(VuePlugin)

$('.project-detail.menu .item').tab()

$(document).ready(() => {
  const openApiVisualizer = $('#openapi-visualizer')

  if(openApiVisualizer.length) {
    const repoInputApp = new Vue({
      el: '#openapi-visualizer',
      data: {
        specs: []
      },
      components: {
        'swagger-ui': SwaggerUI
      },
    })

    const apiDefinitionItem = $('.item[data-tab="openapi"]')

    function cancelApiLoader() {
      apiDefinitionItem.removeClass('loading')
      apiDefinitionItem.addClass('disabled')
      apiDefinitionItem.css('pointer-events', 'all')
      apiDefinitionItem.unbind('click')
      apiDefinitionItem.popup(
        {
          html: `
            <h3 class="ui header">API Schema not available</h3>
            <p>The repository either doesn't contain any OpenAPI definitions, or the ones available couldn't be parsed correctly</p>
            <p>Learn more about <a href="https://swagger.io/docs/specification/about/">OpenAPI</a></p>
          `,
          position: 'bottom left',
          transition: 'fade up',
          hoverable: true,
          variation: 'wide'
        }
      )
    }

    $.get(openApiVisualizer.data('url'))
    .done((response) => {
      if(response.length > 0) {
        repoInputApp.specs = response
        apiDefinitionItem.removeClass('loading')
      } else {
        cancelApiLoader()
      }
    })
    .fail(() => {
      cancelApiLoader()
    })
  }

  const pagerdutyDetailsContainer = $('#pagerduty-details-container')

  if(pagerdutyDetailsContainer.length) {
    $.get(pagerdutyDetailsContainer.data('url'))
    .done((response) => {
      let template = $('#pagerduty-details').html()
      pagerdutyDetailsContainer.html(Mustache.render(template, response))
      pagerdutyDetailsContainer.removeClass('loading')
      $('.statistic').popup({
        transition: 'fade down',
        exclusive: true,
        position: 'top center'
      })
    })
    .fail(() => {
      showSnackbar('Failed fetching pagerduty details')
      pagerdutyDetailsContainer.remove()
    })
  }

  $('.histogram .hitbox').popup({
    transition: 'fade down',
    position: 'top center',
    on: 'hover',
    exclusive: true,
    delay: {
      show: 250,
      hide: 0
    },
    className: {
      popup: 'ui histogram-popup popup'
    }
  })

  $('#issue-description').popup({
    transition: 'fade down',
    position: 'left center',
    on: 'click',
    exclusive: true,
    delay: {
      show: 250,
      hide: 0
    }
  })
})
