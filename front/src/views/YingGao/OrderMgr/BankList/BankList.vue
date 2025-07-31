<script setup lang="tsx">
import { reactive, ref, unref } from 'vue'
import { getBKListApi, imPortCsvDataApi } from '@/api/yinggao/orderMgr/banklist'
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
  // 获取代收订单列表
  fetchDataApi: async () => {
    const { pageSize, currentPage } = tableState
    const res = await getBKListApi({
      page: unref(currentPage),
      limit: unref(pageSize),
      ...unref(searchParams)
    })
    return {
      list: res.data || [],
      total: res.count || 0
    }
  },
  

})

const { dataList, loading, total, pageSize, currentPage } = tableState
const { getList, delList } = tableMethods



const tableColumns = reactive<TableColumn[]>([
  {
    field: 'bank_name',
    label: '银行名称',
    show: true,
	width: 120,
	fixed: 'left'
  },
  {
    field: 'channel_code',
    label: '通道code',
    show: true,
	width: 120,
	fixed: 'left'
  },
  {
    field: 'bank_account',
    label: '银行账号',
    show: true,
	width: 160
  },
  {
    field: 'bank_utr',
    label: '银行UTR',
    show: true,
	width: 160
  },
  // {
  //   field: 'random_number',
  //   label: '随机数',
  //   show: true,
  // 	width: 100
  // },
  {
    field: 'amount',
    label: '金额',
    show: true,
	width: 120
  },
  {
    field: 'account_balance',
    label: '账号余额',
    show: true,
	width: 120
  },
 //  {
 //    field: 'random_number',
 //    label: '随机数',
 //    show: true,
	// width: 180
 //  },
  {
    field: 'create_datetime',
    label: '交易时间',
    show: true,
	width: 180
  },
  {
    field: 'trading_info',
    label: '交易信息',
    show: true,
	width: 480
  },
  {
    field: 'info_sources',
    label: '信息来源',
    show: true,
	// fixed: 'right',
	width: 120,
    slots: {
      default: (data: any) => {
        const row = data.row
  		// 信息来源: sms:短信上传, crawler:爬虫, backend: 后台上传"
  		if(row.info_sources == 'sms') {
  			return (<><span><el-button type="primary" size="small" plain>短信上传</el-button></span></>)
  		}
  		if(row.info_sources == 'crawler'){
  			return (<><span><el-button type="success" size="small" plain>爬虫</el-button></span></>)
  		}
  		if(row.info_sources == 'backend'){
  			return (<><span><el-button type="danger" size="small" plain>后台上传</el-button></span></>)
  		}
  		
      }
    }
  },
 //  {
 //    field: 'match_type',
 //    label: '匹配类型',
	// fixed: 'right',
 //    show: true,
	// width: 120,
	// slots: {
	//   default: (data: any) => {
	//     const row = data.row
	// 	// 匹配类型: auto:自动撞库, manual:手动补单,unmatch:未匹配,robot:机器人补单,active: 主动填写"
	// 	if(row.match_type == 'auto') {
	// 		return (<><span><el-button type="primary" size="small" plain>自动撞库</el-button></span></>)
	// 	}
	// 	if(row.match_type == 'manual'){
	// 		return (<><span><el-button type="success" size="small" plain>手动补单</el-button></span></>)
	// 	}
	// 	if(row.match_type == 'unmatch'){
	// 		return (<><span><el-button type="danger" size="small" plain>未匹配</el-button></span></>)
	// 	}
	// 	if(row.match_type == 'robot'){
	// 		return (<><span><el-button type="danger" size="small" plain>机器人补单</el-button></span></>)
	// 	}
	// 	if(row.match_type == 'active'){
	// 		return (<><span><el-button type="danger" size="small" plain>主动填写</el-button></span></>)
	// 	}
		
	//   }
	// }
 //  },
 //  {
 //    field: 'collection_type',
 //    label: '收款类型',
	// fixed: 'right',
 //    show: true,
	// width: 120,
	// slots: {
	//   default: (data: any) => {
	//     const row = data.row
	// 	// 收款类型: entry:入账，extract:提取
	// 	if(row.collection_type == 'entry') {
	// 		return (<><span><el-button type="primary" size="small" plain>入账</el-button></span></>)
	// 	}
	// 	if(row.collection_type == 'extract'){
	// 		return (<><span><el-button type="success" size="small" plain>提取</el-button></span></>)
	// 	}		
	//   }
	// }
 //  },
 
 
 //  {
 //    field: 'create_datetime',
 //    label: '创建时间',
 //    show: true,
	// width: 120
 //  },
 //  {
 //    field: 'action',
 //    width: '160px',
 //    label: '操作',
	// fixed: 'right',
 //    show: true,
 //    slots: {
 //      default: (data: any) => {
 //        const row = data.row
 //        return (
 //          <>
	// 		<BaseButton
	// 		  type="primary"
	// 		  v-hasPermi="merchant.channel.delete"
	// 		  loading={delLoading.value}
	// 		  link
	// 		  size="small"
	// 		  onClick={() => delData(row)}
	// 		>
	// 		  手动补单
	// 		</BaseButton>
 //          </>
 //        )
 //      }
 //    }
 //  }
])

const searchSchema = reactive<FormSchema[]>([
  {
    field: 'bank_name',
    label: '银行名称',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'channel_code',
    label: '通道名称',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  {
    field: 'bank_utr',
    label: 'UTR',
    component: 'Input',
    componentProps: {
      clearable: false,
      style: {
        width: '214px'
      }
    }
  },
  // {
  //   field: 'order_id',
  //   label: '订单号',
  //   component: 'Input',
  //   componentProps: {
  //     clearable: false,
  //     style: {
  //       width: '214px'
  //     }
  //   }
  // },

  {
    field: 'match_type',
    label: '匹配类型',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '自动撞库',
          value: 'auto'
        },
        {
          label: '手动补单',
          value: 'manual'
        },
		{
		  label: '未匹配',
		  value: 'unmatch'
		},
		{
		  label: '机器人补单',
		  value: 'robot'
		},
		{
		  label: '主动填写',
		  value: 'active'
		}
      ]
    }
  },
  {
    field: 'collection_type',
    label: '收款类型',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '入账',
          value: 'entry'
        },
        {
          label: '提取',
          value: 'extract'
        }
      ]
    }
  },
  {
    field: 'info_sources',
    label: '信息来源',
    component: 'Select',
    componentProps: {
      style: {
        width: '214px'
      },
      options: [
        {
          label: '短信上传',
          value: 'sms'
        },
        {
          label: '爬虫',
          value: 'crawler'
        },
		{
		  label: '后台上传',
		  value: 'backend'
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
const bank_name = ref()

const writeRef = ref<ComponentRef<typeof Write>>()

const saveLoading = ref(false)

// const editAction = async (row: any) => {
//   const res = await getChannelByIdApi(row.id)
//   if (res) {
//     dialogTitle.value = '编辑'
//     actionType.value = 'edit'
//     currentRow.value = res.data
//     dialogVisible.value = true
//   }
// }

const addAction = (value) => {
  bank_name.value = value
  dialogTitle.value = '上传'+value
  actionType.value = 'add'
  currentRow.value = undefined
  dialogVisible.value = true
}

const save = async () => {
  const write = unref(writeRef)
  const formData = await write?.submit()
  // console.log("formData------------->", formData)

  if (formData) {
	const jsonData = {
	  	"bank_name": bank_name.value,
	  	"bank_account": formData.bank_account,
	  	"channel_code": formData.channel_code,
	  	"file_name": formData.upload_file[0].name
	}
    saveLoading.value = true
    try {
      const res = ref({})
      if (actionType.value === 'add') {
        res.value = await imPortCsvDataApi(jsonData)
        if (res.value) {
          dialogVisible.value = false
          getList()
        }
      } else if (actionType.value === 'edit') {
        // res.value = await editChannelApi(formData)
        // if (res.value) {
        //   dialogVisible.value = false
        //   getList()
        // }
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
	
	
		<!-- v-hasPermi="['merchant.channel.create']" -->
      <!-- <template #toolbar>
        <ElRow :gutter="10">
          <ElCol :span="1.5">
			<BaseButton type="primary"  @click="addAction('iob')">上传IOB(csv)</BaseButton>
			<BaseButton type="primary"  @click="addAction('bom')">上传BOM(xls)</BaseButton>
			<BaseButton type="primary"  @click="addAction('pfed')">上传PFED(csv)</BaseButton>
			<BaseButton type="primary"  @click="addAction('cab')">上传CAB(csv)</BaseButton>
			<BaseButton type="primary"  @click="addAction('idbi-enterprise')">上传IDBI企业用户</BaseButton>
			<BaseButton type="primary"  @click="addAction('idbi-ordinary')">上传IDBI普通用户</BaseButton>
          </ElCol>
        </ElRow>
      </template> -->
	  
    </Table>
  </ContentWrap>

 <Dialog v-model="dialogVisible" :title="dialogTitle" :height="300">
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
