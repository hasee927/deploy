<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import {
  getChannelListApi,
  getChannelByIdApi,
  addChannelApi,
  editChannelApi,
  delChannelApi
} from '@/api/yinggao/merchantMgr/channel'
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
  // 获取通道列表
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getChannelListApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      ...unref(searchParams)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  
  // 删除通道
  fetchDelApi: async (value) => {
    const res = await delChannelApi(value)
    return res.code === 200
  }
})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList } = tableMethods



const tableColumns = reactive<TableColumn[]>([
  {
    field: 'channel_code',
    label: '通道code',
    show: true,
    width: '120px',
    fixed: 'left'
  },
  {
    field: 'pay_company',
    label: '代付公司',
    show: true,
	width: '100px',
  },
  {
    field: 'channel_name',
    label: '通道名称',
    show: true,
	width: '150px',
  },


  {
    field: 'channel_type',
    label: '通道类型',
    show: true,
	width: '120px',
	slots: {
	  default: (data: any) => {
	    const row = data.row
		if(row.channel_type == 1) {
			return (<><span><el-button type="success" round size="small">代收通道</el-button></span></>)
		}else{
			return (<><span><el-button type="danger" round size="small">代付通道</el-button></span></>)
		}
	  }
	}
  },
 //  {
 //    field: 'amount_type',
 //    label: '通道金额类型',
 //    show: true,
	// width: '120px',
 //  	slots: {
 //  	  default: (data: any) => {
 //  	    const row = data.row
	// 	if(row.amount_type == 1) {
	// 		return (<><span><el-button type="primary" size="small" plain>大金额</el-button></span></>)
	// 	}else{
	// 		return (<><span><el-button type="warning" size="small" plain>小金额</el-button></span></>)
	// 	}
 //  	  }
 //  	}
 //  },
  {
    field: 'channel_status',
    label: '通道状态',
    show: true,
	width: '100px',
    slots: {
      default: (data: any) => {
        const row = data.row
		if(row.channel_status == 1) {
			return (<><span><el-button type="success" size="small" plain>正常</el-button></span></>)
		}else{
			return (<><span><el-button type="danger" size="small" plain>异常</el-button></span></>)
		}
      }
    }
  },
  {
    field: 'pay_gw_addr',
    label: '代付网关地址',
    show: true,
    width: '200px',
  },
  {
    field: 'pay_gw_check_status_addr',
    label: '代付网关状态检查地址',
    show: true,
    width: '200px',
  },
  {
    field: 'pay_gw_merchant_id',
    label: '代付网关商户名称(ID)',
    show: true,
    width: '200px',
  },
  {
    field: 'pay_gw_id',
    label: '代付网关ID(key)',
    show: true,
    width: '200px',
  },
  {
    field: 'pay_gw_token',
    label: '代付网关TOKEN(secret)',
    show: true,
    width: '200px',
  },  
  {
    field: 'pay_gw_callback_id',
    label: '代付网关回调地址ID',
    show: true,
    width: '200px',
  },
  {
    field: 'pay_gw_spare',
    label: '支付网关备用字段ID',
    show: true,
    width: '200px',
  },
  
 //  {
 //    field: 'disabled',
 //    label: '是否禁用',
 //    show: true,
	// width: '120px',
 //    slots: {
 //      default: (data: any) => {
 //        const row = data.row
 //        return (
 //          <>
 //            <ElSwitch modelValue={row.disabled} />
 //          </>
 //        )
 //      }
 //    }
 //  },

  {
    field: 'create_datetime',
    label: '创建时间',
    show: true,
	width: '170px',
  },
  {
    field: 'remark',
    label: '备注',
    show: true,
	width: '170px',
  },
  {
    field: 'action',
    width: '120px',
    label: '操作',
    show: true,
	fixed: 'right',
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
    field: 'channel_code',
    label: '通道code',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'channel_type',
    label: '通道类型',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '代收通道',
          value: 1
        },
        {
          label: '代付通道',
          value: 2
        }
      ]
    }
  },

  {
    field: 'channel_status',
    label: '通道状态',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '正常',
          value: 1
        },
        {
          label: '异常',
          value: 2
        }
      ]
    }
  }
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
  const res = await getChannelByIdApi(row.id)
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
        res.value = await addChannelApi(formData)
        if (res.value) {
          dialogVisible.value = false
          getList()
        }
      } else if (actionType.value === 'edit') {
        res.value = await editChannelApi(formData)
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
      :pagination="{total}"
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
