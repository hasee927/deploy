<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import {
  getBotListApi,
  getBotByIdApi,
  addBotApi,
  editBotApi,
  delBotApi
} from '@/api/yinggao/AttachmentService/botlist'
import { useTable } from '@/hooks/web/useTable'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ElSwitch } from 'element-plus'
import { Search } from '@/components/Search'
import { FormSchema } from '@/components/Form'
import { ContentWrap } from '@/components/ContentWrap'
import Write from './components/Write.vue'
import { Dialog } from '@/components/Dialog'
// import { DictDetail, selectDictLabel } from '@/utils/dict'
// import { useDictStore } from '@/store/modules/dict'
import { BaseButton } from '@/components/Button'



const { t } = useI18n()

const { tableRegister, tableState, tableMethods } = useTable({
  // 获取机器人列表
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getBotListApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      ...unref(searchParams)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  
  // 删除机器人
  fetchDelApi: async (value) => {
    const res = await delBotApi(value)
    return res.code === 200
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList } = tableMethods



const tableColumns = reactive<TableColumn[]>([
  {
    field: 'chat_id',
    label: '群聊ID',
    show: true,
	width: '180px',
  },
  {
    field: 'name',
    label: '群名称',
    show: true,
  	width: '180px',
  },
  {
    field: 'token',
    label: '机器人TOKEN',
    show: true,
	width: '320px',
  },
  {
    field: 'user_to',
    label: '用途',
    show: true,
	width: '260px',
  },
  {
    field: 'command',
    label: '机器人命令',
    show: true,
    width: '280px',
  },


  {
    field: 'bot_sign',
    label: '机器人标识',
	width: '220px',
    show: true
  },
  {
    field: 'remark',
    label: '备注',
	width: '220px',
    show: true,
  
  },
  {
    field: 'action',
    width: '140px',
    label: '操作',
	fixed: 'right',
    show: true,
    slots: {
      default: (data: any) => {
        const row = data.row
        return (
          <>
            <BaseButton
              type="primary"
			  v-hasPermi="merchant.channel.update"
              link
              size="small"
              onClick={() => editAction(row)}
            >
              编辑
            </BaseButton>
            <BaseButton
              type="danger"
			  v-hasPermi="merchant.channel.delete"
              loading={delLoading.value}
              link
              size="small"
              onClick={() => delData(row)}
            >
              删除
            </BaseButton>
          </>
        )
      }
    }
  }
])

const searchSchema = reactive<FormSchema[]>([
  {
    field: 'chat_id',
    label: '群聊ID',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'name',
    label: '群名称',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'bot_sign',
    label: '机器人标识',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  
])

const searchParams = ref({})
const setSearchParams = (data: any) => {
  currentPage.value = 1
  searchParams.value = data
  getList()
}

const delLoading = ref(false)

const delData = async (row: any) => {
  delLoading.value = true
  await delList(true, [row.id]).finally(() => {
    delLoading.value = false
  })
}



const dialogVisible = ref(false)
const dialogTitle = ref('')

const currentRow = ref()
const actionType = ref('')

const writeRef = ref<ComponentRef<typeof Write>>()

const saveLoading = ref(false)

const editAction = async (row: any) => {
  const res = await getBotByIdApi(row.id)
  if (res) {
    dialogTitle.value = '编辑'
    actionType.value = 'edit'
    currentRow.value = res.data
    dialogVisible.value = true
  }
}

const addAction = () => {
  dialogTitle.value = '新增'
  actionType.value = 'add'
  currentRow.value = undefined
  dialogVisible.value = true
}

const save = async () => {
  const write = unref(writeRef)
  const formData = await write?.submit()
  console.log("formData------------->", formData)
  if (formData) {
    saveLoading.value = true
    try {
      const res = ref({})
      if (actionType.value === 'add') {
        res.value = await addBotApi(formData)
        if (res.value) {
          dialogVisible.value = false
          getList()
        }
      } else if (actionType.value === 'edit') {
        res.value = await editBotApi(formData)
        if (res.value) {
          dialogVisible.value = false
          getList()
        }
      }
    } finally {
      saveLoading.value = false
    }
  }
}


</script>

<template>
  <ContentWrap>
    <Search :schema="searchSchema" @reset="setSearchParams" @search="setSearchParams" />
    <Table
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      showAction
      :columns="tableColumns"
      default-expand-all
      node-key="id"
      :data="dataList"
      :loading="loading"
      :pagination="{
        total
      }"
      @register="tableRegister"
      @refresh="getList"
    >
      <template #toolbar>
        <ElRow :gutter="10">
          <ElCol :span="1.5">
            <BaseButton type="primary" v-hasPermi="['merchant.channel.create']" @click="addAction">新增</BaseButton>
          </ElCol>
        </ElRow>
      </template>
    </Table>
  </ContentWrap>

  <Dialog v-model="dialogVisible" :title="dialogTitle" :height="650">
    <Write ref="writeRef" :current-row="currentRow" />

    <template #footer>
      <BaseButton type="primary" :loading="saveLoading" @click="save">
        {{ t('exampleDemo.save') }}
      </BaseButton>
      <BaseButton @click="dialogVisible = false">{{ t('dialogDemo.close') }}</BaseButton>
    </template>
  </Dialog>

  <!-- <AuthManage ref="authManageRef" :current-row="currentRow" @get-list="getList" /> -->
</template>
