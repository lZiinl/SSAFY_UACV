import { defineStore } from "pinia"
import { computed, ref } from "vue"
import { useRouter } from "vue-router"

import axios from "axios"

export const userAdminStore = defineStore('admin', () => {

  const router = useRouter()

  //== 계정생성 ==//
  const signUp = function (payload) {
    const { username, password1, password2, memberRole, rnk, m_id } = payload
    axios({
      method: 'post',
      url: '/member/create',
      data: {
        username, password1, password2, memberRole, rnk, m_id
      }
    })
      .then((response) => {
        alert("계정 생성 완료")
        router.push('/user_management')
      })
      .catch((error) => {
        console.log(error)
      })
  }

  //== 권한 변경 ==//
  const updateRole = function (payload) {

    const { username, memberRole } = payload

    axios({
      method: 'put',
      url: '/member/update/role',
      data: {
        username, memberRole
      },
      headers: {
        Authorization: `Bearer ${sessionStorage.getItem("token")}`
      }
    })
      .then((response) => {
        router.go(0)
        alert("권한이 변경되었습니다.")
      })
      .catch((error) => {
        console.log(error)
      })
  }

  //== 회원 삭제 ==//
  const deleteMember = function (memberId) {
    axios({
      method: 'delete',
      url: `/member/delete/${memberId}`,
      headers: {
        Authorization: `Bearer ${sessionStorage.getItem("token")}`
      }
    })
      .then((response) => {
        console.log(response.data)

        router.push({
          path: '/memberList'
        })
      })
      .catch((error) => {
        console.log(error)
      })
  }

  //== memberList 저장 ==//
  const members = ref(null)

  //== 회원 리스트 출력 ==//
  const memberList = async function () {

    try {
      const response = await axios({
        method: 'get',
        url: '/member/list'
      })
      members.value = response.data

    } catch (error) {
      console.log(error)
      throw error
    }

    return members.value
  }

  //== members의 유뮤 ==//
  const isMembers = computed(() => {
    if (members.value) {
      if (members.value.length === 0) {
        return false
      } else {
        return true
      }
    }
  })

  //== 찾은 회원 정보 저장 ==//
  const memberInfo = ref(null)

  //== 해당 회원 정보 ==//
  const findMember = async function (memberId) {

    try {
      const response = await axios({
        method: 'get',
        url: `/member/${memberId}`,
        headers: {
          Authorization: `Bearer ${sessionStorage.getItem("token")}`
        }
      })

      memberInfo.value = response.data
    } catch (error) {
      console.log(error)
      throw error
    }

    return memberInfo.value
  }

  return {
    signUp, memberList, findMember, updateRole, deleteMember,
    members, isMembers, memberInfo
  }
})